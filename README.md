# AI-Powered Supply Chain Disruption Prediction Platform

A Flask-based AI platform that predicts supply chain disruption risk, visualizes trends, and now includes production-focused engineering upgrades:
- Structured app package (`app/`)
- Persistent prediction logging with SQLAlchemy
- Versioned REST API (`/api/v1`)
- Security hardening (CSRF, headers, rate limiting, validation)
- Automated tests with `pytest`
- CI workflow via GitHub Actions

## Architecture

```text
app.py (entrypoint)
  -> app.create_app()
    -> app/routes/web.py      # HTML pages
    -> app/routes/api.py      # REST API
    -> app/services/          # Prediction + recommendation logic
    -> app/models.py          # DB models (PredictionLog)
    -> app/artifacts.py       # Model/data loading
```

## Features

- Risk prediction from event details
- Dashboard for operational metrics
- Model performance page (accuracy/precision/recall/F1/ROC-AUC)
- Analytics trend visualizations
- API endpoints for integration
- Persistent logs of all prediction requests

## Security Controls Implemented

- Input validation for web + API prediction payloads
- CSRF protection for server-rendered forms
- Security headers with `Flask-Talisman`
- Rate limiting on prediction API
- Request size limit (`MAX_CONTENT_LENGTH`)
- ORM-based persistence to reduce SQL injection risk
- Optional restricted CORS for API clients

## Prerequisites

- Python 3.10+
- pip

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate training data:
```bash
python generate_data.py
```

3. Train and save model artifacts:
```bash
python train_model.py
```

4. Run the app:
```bash
python app.py
```

The app is available at `http://127.0.0.1:5000`.

## Environment Variables

- `FLASK_ENV`: `development` | `testing` | `production`
- `FLASK_DEBUG`: `true` or `false`
- `PORT`: App port (default `5000`)
- `SECRET_KEY`: Flask secret key (set strongly in production)
- `DATABASE_URL`: SQLAlchemy DB URL (defaults to local SQLite)
- `TALISMAN_FORCE_HTTPS`: `true`/`false`
- `CORS_ORIGINS`: comma-separated API origins
- `RATELIMIT_STORAGE_URI`: limiter backend URI (default `memory://`)

## Database

The app auto-creates required tables at startup for MVP convenience.

### Migration-ready setup
`Flask-Migrate` is integrated and an initial migration is included in `migrations/versions/`.

To apply migrations on a fresh database:
```bash
export FLASK_APP=app.py
flask db upgrade
```

If your local DB was already auto-created before migrations were initialized, align it once with:
```bash
export FLASK_APP=app.py
flask db stamp head
```

## REST API

Base URL: `/api/v1`

### `GET /api/v1/health`
Health and setup status.

### `POST /api/v1/predict`
Predict disruption risk.

Request JSON example:
```json
{
  "event_type": "Port Congestion",
  "severity_level": "High",
  "cause": "Infrastructure Failure",
  "country": "India",
  "financial_impact": 125000
}
```

Response shape:
```json
{
  "input": {"...": "..."},
  "result": {
    "prediction": 1,
    "prediction_text": "DISRUPTION",
    "probability": 0.9211,
    "risk_level": "Very High",
    "recommendations": ["..."]
  }
}
```

### `GET /api/v1/metrics`
Returns model metrics and best-model summary.

### `GET /api/v1/analytics/trends`
Returns monthly disruptions, total events, and disruption rate.

## Testing

Run tests locally:
```bash
pytest -q
```

Current automated tests cover:
- Core page availability
- API health
- API input validation
- Prediction endpoint response contract
- Prediction logging in DB
- Security header presence

## CI

GitHub Actions workflow at `.github/workflows/ci.yml` runs tests on push and PR.

## Deployment

- Render build command: `./build.sh`
- Start command: `gunicorn app:app`

## Project Structure

```text
app/
  __init__.py
  artifacts.py
  config.py
  extensions.py
  models.py
  routes/
    api.py
    web.py
  services/
    prediction_service.py
tests/
.github/workflows/ci.yml
app.py
generate_data.py
train_model.py
```
