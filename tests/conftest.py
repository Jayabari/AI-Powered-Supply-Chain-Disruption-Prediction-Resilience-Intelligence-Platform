from __future__ import annotations

import pytest

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
