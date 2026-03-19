from __future__ import annotations

from app.artifacts import get_data
from app.extensions import db
from app.models import PredictionLog, User


def _register_and_login(client):
    register_response = client.post(
        "/register",
        data={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
        follow_redirects=True,
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200


def test_dashboard_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dashboard Overview" in response.data


def test_predict_page_loads(client):
    response = client.get("/predict")
    assert response.status_code == 302


def test_api_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"


def test_api_predict_rejects_invalid_payload(client):
    _register_and_login(client)

    response = client.post(
        "/api/v1/predict",
        json={
            "event_type": "InvalidType",
            "severity_level": "High",
            "cause": "Political",
            "country": "USA",
            "financial_impact": 80000,
        },
    )
    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload


def test_api_predict_logs_prediction(client, app_instance):
    _register_and_login(client)

    data = get_data()
    sample = data.iloc[0]

    payload = {
        "event_type": sample["event_type"],
        "severity_level": sample["severity_level"],
        "cause": sample["cause"],
        "country": sample["country"],
        "financial_impact": float(sample["financial_impact"]),
    }

    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    body = response.get_json()

    assert "result" in body
    assert body["result"]["prediction_text"] in {"DISRUPTION", "MANAGEABLE"}
    assert 0.0 <= body["result"]["probability"] <= 1.0

    with app_instance.app_context():
        total_logs = PredictionLog.query.count()
        assert total_logs >= 1


def test_security_headers_present(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"


def test_register_creates_user(client, app_instance):
    response = client.post(
        "/register",
        data={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "securepass",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app_instance.app_context():
        user = db.session.query(User).filter_by(email="alice@example.com").first()
        assert user is not None
        assert user.role == "user"


def test_protected_web_routes_require_login(client):
    predict_response = client.get("/predict")
    performance_response = client.get("/performance")
    analytics_response = client.get("/analytics")

    assert predict_response.status_code == 302
    assert performance_response.status_code == 302
    assert analytics_response.status_code == 302


def test_protected_api_requires_login(client):
    response = client.post("/api/v1/predict", json={})
    assert response.status_code == 401
