from __future__ import annotations

from typing import Any

import pandas as pd


class ValidationError(ValueError):
    pass


def _validate_value(raw_value: str, allowed: list[str], field: str) -> str:
    if raw_value not in allowed:
        raise ValidationError(f"Invalid value for {field}.")
    return raw_value


def parse_prediction_input(payload: dict[str, Any], data: pd.DataFrame) -> dict[str, Any]:
    event_types = sorted(data["event_type"].unique())
    severity_levels = ["Low", "Medium", "High", "Critical"]
    causes = sorted(data["cause"].unique())
    countries = sorted(data["country"].unique())

    event_type = _validate_value(str(payload.get("event_type", event_types[0])), event_types, "event_type")
    severity_level = _validate_value(
        str(payload.get("severity_level", "Medium")),
        severity_levels,
        "severity_level",
    )
    cause = _validate_value(str(payload.get("cause", causes[0])), causes, "cause")
    country = _validate_value(str(payload.get("country", countries[0])), countries, "country")

    raw_impact = payload.get("financial_impact", 50000)
    try:
        financial_impact = float(raw_impact)
    except (TypeError, ValueError) as exc:
        raise ValidationError("financial_impact must be a number.") from exc

    if financial_impact < 1000 or financial_impact > 5000000:
        raise ValidationError("financial_impact must be between 1,000 and 5,000,000.")

    return {
        "event_type": event_type,
        "severity_level": severity_level,
        "cause": cause,
        "country": country,
        "financial_impact": financial_impact,
    }


def build_options(data: pd.DataFrame) -> dict[str, list[str]]:
    return {
        "event_type": sorted(data["event_type"].unique()),
        "severity_level": ["Low", "Medium", "High", "Critical"],
        "cause": sorted(data["cause"].unique()),
        "country": sorted(data["country"].unique()),
    }
