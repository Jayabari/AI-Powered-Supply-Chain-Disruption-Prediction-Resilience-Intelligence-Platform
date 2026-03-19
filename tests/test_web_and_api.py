from __future__ import annotations

from app.artifacts import get_data
from app.models import PredictionLog


def test_dashboard_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dashboard Overview" in response.data


def test_predict_page_loads(client):
    response = client.get("/predict")
    assert response.status_code == 200
    assert b"Predict Disruption Risk" in response.data


def test_api_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"


def test_api_predict_rejects_invalid_payload(client):
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
