from __future__ import annotations

from datetime import UTC, datetime

from .extensions import db


class PredictionLog(db.Model):
    __tablename__ = "prediction_logs"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    severity_level = db.Column(db.String(20), nullable=False)
    cause = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    financial_impact = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    probability = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(20), nullable=False, default="web")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
