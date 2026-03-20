from __future__ import annotations

import pandas as pd
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.artifacts import get_data, load_model_artifacts, setup_ready
from app.extensions import db
from app.models import User
from app.services.prediction_service import log_prediction, run_prediction
from app.validators import ValidationError, build_options, parse_prediction_input


def register_web_routes(app):
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

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not name:
                flash("Name is required.", "error")
                return render_template("register.html")
            if "@" not in email:
                flash("A valid email is required.", "error")
                return render_template("register.html")
            if len(password) < 8:
                flash("Password must be at least 8 characters.", "error")
                return render_template("register.html")

            existing = User.query.filter_by(email=email).first()
            if existing:
                flash("Email already registered. Please login.", "error")
                return render_template("register.html")

            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash("Account created successfully. Please login.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_password(password):
                flash("Invalid email or password.", "error")
                return render_template("login.html")

            login_user(user)
            flash("Welcome back.", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))

    @app.route("/predict", methods=["GET", "POST"])
    @login_required
    def predict():
        if not setup_ready():
            return render_template("setup_required.html")

        data = get_data()
        options = build_options(data)

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
            try:
                form_values = parse_prediction_input(request.form, data)
                result = run_prediction(form_values)
                log_prediction(form_values, result, source="web")
            except ValidationError as exc:
                flash(str(exc), "error")
                form_values = defaults

        return render_template(
            "predict.html",
            options=options,
            result=result,
            form_values=form_values,
        )

    @app.route("/performance")
    @login_required
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
    @login_required
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

        country_risk = data.groupby("country")["disruption"].mean().sort_values(ascending=False).head(10)
        cause_impact = data.groupby("cause")["financial_impact"].sum().sort_values(ascending=False).head(10)

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
