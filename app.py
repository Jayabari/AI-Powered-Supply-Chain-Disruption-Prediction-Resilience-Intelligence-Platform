from __future__ import annotations

import json
import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "supply_chain_events.csv"
MODEL_DIR = BASE_DIR / "model"


app = Flask(__name__)


def load_model_artifacts():
    model = joblib.load(MODEL_DIR / "disruption_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    encoders = joblib.load(MODEL_DIR / "encoders.pkl")
    features = joblib.load(MODEL_DIR / "features.pkl")
    with open(MODEL_DIR / "metrics.json", "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return model, scaler, encoders, features, metrics


def get_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def setup_ready() -> bool:
    required_files = [
        DATA_PATH,
        MODEL_DIR / "disruption_model.pkl",
        MODEL_DIR / "scaler.pkl",
        MODEL_DIR / "encoders.pkl",
        MODEL_DIR / "features.pkl",
        MODEL_DIR / "metrics.json",
    ]
    return all(path.exists() for path in required_files)


def parse_prediction_form(form_data, data: pd.DataFrame):
    return {
        "event_type": form_data.get("event_type", sorted(data["event_type"].unique())[0]),
        "severity_level": form_data.get("severity_level", "Medium"),
        "cause": form_data.get("cause", sorted(data["cause"].unique())[0]),
        "country": form_data.get("country", sorted(data["country"].unique())[0]),
        "financial_impact": float(form_data.get("financial_impact", 50000)),
    }


def build_recommendations(form_values, prediction: int):
    severity = form_values["severity_level"]
    event_type = form_values["event_type"]
    cause = form_values["cause"]
    financial_impact = form_values["financial_impact"]

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


@app.context_processor
def inject_global_metrics():
    if not setup_ready():
        return {"global_model_info": None}

    try:
        _, _, _, _, metrics = load_model_artifacts()
        best = metrics["best_model"]
        best_metrics = metrics["models_performance"][best]
        return {
            "global_model_info": {
                "best_model": best,
                "accuracy": best_metrics["accuracy"] * 100,
                "dataset_size": metrics["dataset_size"],
            }
        }
    except Exception:
        return {"global_model_info": None}


@app.route("/")
def dashboard():
    if not setup_ready():
        return render_template("setup_required.html")

    data = get_data()
    _, _, _, _, metrics = load_model_artifacts()

    total_events = int(len(data))
    disruptions = int(data["disruption"].sum())
    non_disruptions = total_events - disruptions
    avg_impact = float(data["financial_impact"].mean())

    severity_counts = data["severity_level"].value_counts()
    event_counts = data["event_type"].value_counts().head(8)
    top_disruptions = (
        data[data["disruption"] == 1]
        .nlargest(10, "financial_impact")
        [["event_id", "event_date", "event_type", "severity_level", "country", "city", "financial_impact"]]
        .to_dict(orient="records")
    )

    return render_template(
        "dashboard.html",
        metrics=metrics,
        total_events=total_events,
        disruptions=disruptions,
        non_disruptions=non_disruptions,
        disruption_rate=(disruptions / total_events * 100) if total_events else 0,
        avg_impact=avg_impact,
        severity_labels=list(severity_counts.index),
        severity_values=[int(v) for v in severity_counts.values],
        event_labels=list(event_counts.index),
        event_values=[int(v) for v in event_counts.values],
        top_disruptions=top_disruptions,
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if not setup_ready():
        return render_template("setup_required.html")

    data = get_data()
    model, scaler, encoders, features, _ = load_model_artifacts()

    options = {
        "event_type": sorted(data["event_type"].unique()),
        "severity_level": ["Low", "Medium", "High", "Critical"],
        "cause": sorted(data["cause"].unique()),
        "country": sorted(data["country"].unique()),
    }

    defaults = {
        "event_type": options["event_type"][0],
        "severity_level": "Medium",
        "cause": options["cause"][0],
        "country": options["country"][0],
        "financial_impact": 50000,
    }

    result = None
    form_values = defaults

    if request.method == "POST":
        form_values = parse_prediction_form(request.form, data)

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

        result = {
            "prediction": prediction,
            "probability": probability,
            "risk_level": risk_level,
            "prediction_text": "DISRUPTION" if prediction == 1 else "MANAGEABLE",
            "status_class": "bad" if prediction == 1 else "good",
            "recommendations": build_recommendations(form_values, prediction),
        }

    return render_template(
        "predict.html",
        options=options,
        result=result,
        form_values=form_values,
    )


@app.route("/performance")
def performance():
    if not setup_ready():
        return render_template("setup_required.html")

    _, _, _, _, metrics = load_model_artifacts()
    model_rows = []
    for model_name, values in metrics["models_performance"].items():
        model_rows.append(
            {
                "model": model_name,
                "accuracy": values["accuracy"] * 100,
                "precision": values["precision"] * 100,
                "recall": values["recall"] * 100,
                "f1_score": values["f1_score"] * 100,
                "roc_auc": values["roc_auc"] * 100,
            }
        )

    best = metrics["best_model"]
    confusion = metrics["models_performance"][best]["confusion_matrix"]

    return render_template(
        "performance.html",
        metrics=metrics,
        model_rows=model_rows,
        confusion=confusion,
        chart_labels=[row["model"] for row in model_rows],
        chart_f1=[round(row["f1_score"], 2) for row in model_rows],
    )


@app.route("/analytics")
def analytics():
    if not setup_ready():
        return render_template("setup_required.html")

    data = get_data()
    data["event_date"] = pd.to_datetime(data["event_date"])

    monthly = (
        data.groupby(data["event_date"].dt.to_period("M"))["disruption"]
        .agg([("disruptions", "sum"), ("total", "count")])
        .reset_index()
    )
    monthly["event_date"] = monthly["event_date"].astype(str)

    country_risk = (
        data.groupby("country")["disruption"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    cause_impact = (
        data.groupby("cause")["financial_impact"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return render_template(
        "analytics.html",
        monthly_labels=monthly["event_date"].tolist(),
        monthly_total=[int(v) for v in monthly["total"].tolist()],
        monthly_disruptions=[int(v) for v in monthly["disruptions"].tolist()],
        country_labels=country_risk.index.tolist(),
        country_values=[round(v * 100, 1) for v in country_risk.values.tolist()],
        cause_labels=cause_impact.index.tolist(),
        cause_values=[int(v) for v in cause_impact.values.tolist()],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
