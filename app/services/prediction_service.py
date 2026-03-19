from __future__ import annotations

import pandas as pd

from app.artifacts import load_model_artifacts
from app.models import PredictionLog
from app.extensions import db


def build_recommendations(form_values: dict[str, object], prediction: int) -> list[str]:
    severity = str(form_values["severity_level"])
    event_type = str(form_values["event_type"])
    cause = str(form_values["cause"])
    financial_impact = float(form_values["financial_impact"])

    if prediction == 0:
        return [
            "Continue regular monitoring schedule.",
            "Log this event for trend analysis and reporting.",
            "Keep backup suppliers on standby as a preventive step.",
        ]

    recommendations = [
        "Escalate this incident to operations and procurement teams.",
        "Start mitigation plan and monitor updates every 2-4 hours.",
    ]

    if severity in ["High", "Critical"]:
        recommendations.append("Trigger high-severity incident protocol with leadership visibility.")

    if financial_impact > 100000:
        recommendations.append("Initiate financial mitigation plan and reallocation strategy.")

    if event_type in ["Natural Disaster", "Labor Strike", "Port Congestion"]:
        recommendations.append("Activate alternate routing and backup supplier plan immediately.")

    if cause in ["Geopolitical", "Natural Disaster", "Policy Change"]:
        recommendations.append("Send proactive communication to key stakeholders and customers.")

    return recommendations


def run_prediction(form_values: dict[str, object]) -> dict[str, object]:
    model, scaler, encoders, features, _ = load_model_artifacts()

    input_row = {
        "event_type_encoded": encoders["event_type"].transform([form_values["event_type"]])[0],
        "severity_level_encoded": encoders["severity_level"].transform([form_values["severity_level"]])[0],
        "cause_encoded": encoders["cause"].transform([form_values["cause"]])[0],
        "country_encoded": encoders["country"].transform([form_values["country"]])[0],
        "financial_impact": form_values["financial_impact"],
    }

    input_df = pd.DataFrame([input_row])[features]
    input_scaled = scaler.transform(input_df)

    prediction = int(model.predict(input_scaled)[0])
    probability = float(model.predict_proba(input_scaled)[0][1])

    if probability > 0.8:
        risk_level = "Very High"
    elif probability > 0.6:
        risk_level = "High"
    elif probability > 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "prediction": prediction,
        "probability": probability,
        "risk_level": risk_level,
        "prediction_text": "DISRUPTION" if prediction == 1 else "MANAGEABLE",
        "status_class": "bad" if prediction == 1 else "good",
        "recommendations": build_recommendations(form_values, prediction),
    }


def log_prediction(form_values: dict[str, object], result: dict[str, object], source: str) -> None:
    record = PredictionLog(
        event_type=str(form_values["event_type"]),
        severity_level=str(form_values["severity_level"]),
        cause=str(form_values["cause"]),
        country=str(form_values["country"]),
        financial_impact=float(form_values["financial_impact"]),
        prediction=int(result["prediction"]),
        probability=float(result["probability"]),
        risk_level=str(result["risk_level"]),
        source=source,
    )
    db.session.add(record)
    db.session.commit()
