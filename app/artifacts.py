from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "supply_chain_events.csv"
MODEL_DIR = BASE_DIR / "model"


@lru_cache(maxsize=1)
def load_model_artifacts():
    model = joblib.load(MODEL_DIR / "disruption_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    encoders = joblib.load(MODEL_DIR / "encoders.pkl")
    features = joblib.load(MODEL_DIR / "features.pkl")
    with open(MODEL_DIR / "metrics.json", "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return model, scaler, encoders, features, metrics


def clear_artifact_cache() -> None:
    load_model_artifacts.cache_clear()


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
