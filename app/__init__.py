from __future__ import annotations

import logging
import os

from flask import Flask, jsonify, redirect, request, url_for
from flask_cors import CORS
from flask_login import current_user

from app.config import CONFIG_BY_NAME
from app.extensions import csrf, db, limiter, login_manager, migrate, talisman
from app.models import User
from app.routes.api import api_bp
from app.routes.web import register_web_routes


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    config_key = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(CONFIG_BY_NAME.get(config_key, CONFIG_BY_NAME["development"]))

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("login"))

    csp = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "https://cdn.jsdelivr.net"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
    }
    talisman.init_app(app, content_security_policy=csp, force_https=app.config["TALISMAN_FORCE_HTTPS"])

    register_web_routes(app)
    app.register_blueprint(api_bp)
    csrf.exempt(api_bp)

    cors_origins = [origin.strip() for origin in app.config["CORS_ORIGINS"].split(",") if origin.strip()]
    if cors_origins:
        CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(429)
    def handle_rate_limit(error):
        return jsonify({"error": "Rate limit exceeded"}), 429

    @app.errorhandler(403)
    def handle_forbidden(error):
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(500)
    def handle_server_error(error):
        app.logger.exception("Unhandled server error: %s", error)
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        # Keep setup friction low for MVP deployments.
        db.create_all()

    logging.basicConfig(level=logging.INFO)

    return app
