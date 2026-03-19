from __future__ import annotations

import pandas as pd
from flask import Blueprint, jsonify, request

from app.artifacts import get_data, load_model_artifacts, setup_ready
from app.extensions import limiter
from app.services.prediction_service import log_prediction, run_prediction
from app.validators import ValidationError, parse_prediction_input


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok", "setup_ready": setup_ready()})


@api_bp.post("/predict")
@limiter.limit("30 per minute")
def predict_api():
    if not setup_ready():
        return jsonify({"error": "Model setup is incomplete."}), 503

    data = get_data()
    payload = request.get_json(silent=True) or {}

    try:
        form_values = parse_prediction_input(payload, data)
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400

    result = run_prediction(form_values)
    log_prediction(form_values, result, source="api")

    return jsonify({
        "input": form_values,
        "result": {
            "prediction": result["prediction"],
            "prediction_text": result["prediction_text"],
            "probability": round(float(result["probability"]), 4),
            "risk_level": result["risk_level"],
            "recommendations": result["recommendations"],
        },
    })


@api_bp.get("/metrics")
def metrics_api():
    if not setup_ready():
        return jsonify({"error": "Model setup is incomplete."}), 503

    _, _, _, _, metrics = load_model_artifacts()
    best = metrics["best_model"]
    best_metrics = metrics["models_performance"][best]

    return jsonify(
        {
            "best_model": best,
            "dataset_size": metrics["dataset_size"],
            "models_performance": metrics["models_performance"],
            "best_model_summary": {
                "accuracy": best_metrics["accuracy"],
                "precision": best_metrics["precision"],
                "recall": best_metrics["recall"],
                "f1_score": best_metrics["f1_score"],
                "roc_auc": best_metrics["roc_auc"],
            },
        }
    )


@api_bp.get("/analytics/trends")
def analytics_trends_api():
    if not setup_ready():
        return jsonify({"error": "Model setup is incomplete."}), 503

    data = get_data()
    data["event_date"] = pd.to_datetime(data["event_date"])

    monthly = (
        data.groupby(data["event_date"].dt.to_period("M"))["disruption"]
        .agg([("disruptions", "sum"), ("total", "count")])
        .reset_index()
    )
    monthly["event_date"] = monthly["event_date"].astype(str)

    payload = [
        {
            "month": row["event_date"],
            "disruptions": int(row["disruptions"]),
            "total_events": int(row["total"]),
            "disruption_rate": round((row["disruptions"] / row["total"]), 4) if row["total"] else 0.0,
        }
        for _, row in monthly.iterrows()
    ]

    return jsonify({"trends": payload})
