from __future__ import annotations

import pytest

from app import create_app
from app.artifacts import clear_artifact_cache


@pytest.fixture()
def app_instance():
    app = create_app("testing")
    app.config.update(TESTING=True)
    clear_artifact_cache()
    yield app


@pytest.fixture()
def client(app_instance):
    return app_instance.test_client()
