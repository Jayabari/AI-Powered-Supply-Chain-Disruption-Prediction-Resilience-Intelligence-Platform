from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure the repository root is importable in CI and local runs.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from app.artifacts import clear_artifact_cache
from app.extensions import db


@pytest.fixture()
def app_instance():
    app = create_app("testing")
    app.config.update(TESTING=True)
    clear_artifact_cache()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app_instance):
    return app_instance.test_client()
