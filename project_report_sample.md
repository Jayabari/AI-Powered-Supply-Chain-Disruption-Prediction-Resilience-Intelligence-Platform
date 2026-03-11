# Project Synopsis: Supply Chain Disruption Prediction Platform

## 0. Cover

- **Project title:** Supply Chain Disruption Prediction Platform  
- **Team name & ID:** Team (Supply Chain) – *update if you have an official ID*  
- **Repository:** `rishabh-rb/Supply_Chain_Disruption_Prediction`  
- **Institute / Course:** *update as per your institute*  
- **Version:** v1.0  
- **Date:** 2026-03-11  

### Revision history

| Version | Date       | Author   | Change |
|--------:|------------|----------|--------|
| v0.1    | 2026-03-08 | Team     | Initial draft |
| v1.0    | 2026-03-11 | Team     | Finalized synopsis aligned to repo implementation |

---

## 1. Overview

### Problem statement
Organizations face frequent supply chain disruptions (supplier delays, port congestion, labor strikes, natural disasters, geopolitical issues, etc.). Traditional monitoring is often reactive and fragmented, resulting in late detection and delayed mitigation.

### Goal
Build a web-based platform that:
- Trains ML models on supply chain event data
- Predicts disruption risk for new events
- Provides dashboards, analytics, and model-performance reporting to support decision-making

### Non-goals (v1)
- Real-time ERP ingestion and streaming pipelines
- Payment/logistics execution systems (actions are recommendations only)
- Advanced MLOps features like model registry, A/B testing, canary deployments

### Value proposition
- **Early warning signal**: predict disruption probability before impact escalates  
- **Visibility**: dashboard + analytics views for trends and risk drivers  
- **Practical deployment**: simple Flask + Gunicorn deployment (Render-ready)

---

## 2. Scope and Control

### 2.1 In-scope
- Synthetic dataset generation (`generate_data.py`)
- Model training + selection across multiple algorithms (`train_model.py`)
- Saved artifacts for inference (model, scaler, encoders, feature order, metrics)
- Flask application with multi-page UI (`app.py` + `templates/` + `static/`)
  - Dashboard
  - Prediction form + recommendations
  - Model performance comparison view
  - Analytics view (trends + top risk contributors)
- Deployment configuration (`render.yaml`, `Procfile`, `build.sh`)

### 2.2 Out-of-scope
- Real production data integration (ERP/WMS/TMS)
- Role-based access control and authentication
- External API integrations (news/weather/ports) in v1
- Automated mitigation execution workflows (only recommendations)

### 2.3 Assumptions
- Users can run Python 3.8+ locally or deploy on a compatible cloud platform
- Dataset is synthetic for demonstration (as noted in README)
- The “best model” is selected using F1-score from candidate models

### 2.4 Constraints
- Small team capacity and limited time
- Simplicity-first architecture (single Flask app and scripts)
- No heavy infrastructure (no separate DB service required in v1)

### 2.5 Dependencies
- Python runtime + pip
- Libraries: Flask, pandas, numpy, scikit-learn, joblib, gunicorn
- Hosting environment (e.g., Render) for deployment

### 2.6 Acceptance criteria and signoff
**Functional acceptance**
- GIVEN the dataset is generated WHEN training runs THEN artifacts are created in `model/` (pkl + json).
- GIVEN artifacts exist WHEN user opens `/predict` and submits the form THEN disruption probability and risk level are shown.
- GIVEN artifacts exist WHEN user opens `/performance` THEN model comparison metrics display correctly.
- GIVEN artifacts exist WHEN user opens `/analytics` THEN trend and aggregate charts render correctly.

**Operational acceptance**
- App starts successfully using `gunicorn app:app`.
- If artifacts are missing, system shows “setup required” screen (non-crashing behavior).

**Signoff**
- Mentor/Guide approval after demo + report + all P1 bugs resolved.

---

## 3. Stakeholders and RACI

### Key stakeholders
- **Project team:** builds the platform (data generation, ML training, web UI, deployment)
- **Mentor/Instructor:** evaluates deliverables and demo
- **End users (target):** supply chain analysts, procurement managers, operations managers (demo persona)

### RACI table

| Activity | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---------|------------------|-----------------|---------------|--------------|
| Requirements & scope | Jaya, Rishabh | Rishabh | Ananshi | Team |
| UI/UX design + templates | Jaya | Jaya | Rishabh | Team |
| Backend (Flask routes + logic) | Ananshi | Ananshi | Rishabh | Team |
| ML pipeline (data + train + metrics) | Rishabh | Rishabh | Ananshi | Team |
| Deployment pipeline (Render/Gunicorn/build) | Rishabh | Rishabh | Team | Team |
| Integration (UI ↔ backend ↔ model artifacts) | Rishabh | Rishabh | Jaya, Ananshi | Team |
| Testing & bugfix | Team | Rishabh | — | Mentor |

---

## 4. Team and Roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| **Jaya** | Frontend + UI/UX | UI layout and styling (`templates/`, `static/`), UX flows for Dashboard/Predict/Performance/Analytics, form usability, accessibility basics, consistent components (cards/tables/charts sections) |
| **Ananshi** | Backend Developer | Flask routes and server-side logic in `app.py`, data handling, model inference flow correctness, validation, error handling (setup checks), maintainable structure |
| **Rishabh** | Pipeline Dev + ML + Integration | Dataset generation (`generate_data.py`), training pipeline (`train_model.py`) and artifact management, deployment config (`render.yaml`, `Procfile`, `build.sh`), integration of trained artifacts with Flask + UI end-to-end |

---

## 5. Weekwise Plan and Assignments (8-week template)

> Adjust dates to your academic schedule. Below is a realistic plan aligned to this repository’s components.

| Week | Milestones | Jaya (UI/UX) | Ananshi (Backend) | Rishabh (Pipeline/ML/Integration) | Deliverables |
|------|------------|--------------|-------------------|-----------------------------------|-------------|
| 1 | Requirements + KPIs | UX wireframes | Route plan | Define training + artifact format | Scope doc + KPI list |
| 2 | Data & training base | UI skeleton pages | Setup-ready screen | Build data generator | `generate_data.py` ready |
| 3 | Model training v1 | Design dashboard layout | Connect to CSV loader | Implement `train_model.py` | Artifacts saved in `model/` |
| 4 | Prediction flow | Predict form UX | Predict endpoint logic | Integrate artifacts in Flask | `/predict` works end-to-end |
| 5 | Performance view | Tables + charts layout | Performance metrics route | Ensure metrics.json format | `/performance` working |
| 6 | Analytics view | Analytics UI | Aggregation logic | Optimize aggregation + structure | `/analytics` working |
| 7 | Hardening | UI polish + responsiveness | Error handling + refactor | Deployment config test | Bug fixes + test notes |
| 8 | Release | Final UI pass | Final backend pass | Final pipeline/integration | v1 demo + final report |

---

## 6. Users and UX

### 6.1 Personas
- **Analyst Asha (Supply Chain Analyst):** needs quick visibility into disruption trends and top risk drivers.
- **Manager Mohan (Operations/Procurement):** wants a fast “risk score + action recommendation” for an incoming event.

### 6.2 Top user journeys
1. **Risk Monitoring**
   - Home (`/`) → view disruption rate, severity breakdown, and top disruptions.
2. **New Event Prediction**
   - `/predict` → choose event type, severity, cause, country, financial impact → submit → view probability, risk level, and recommended actions.
3. **Model Review**
   - `/performance` → compare models and see confusion matrix for best model.
4. **Trend Analytics**
   - `/analytics` → view monthly disruption trends and top risk countries/causes.

### 6.3 User stories (samples)
- As an analyst, I want to see overall disruption rate so I can understand baseline risk.
- As a manager, I want an interpretable risk level (Low/Medium/High/Very High) so I can decide escalation urgency.
- As a reviewer, I want model comparison metrics so I can justify why a model was selected.

### 6.4 Accessibility & usability
- Clear labels and defaults in forms
- Keyboard navigation for main actions (submit, page links)
- Color contrast for “good/bad” risk labels
- Error-safe screens when setup artifacts are missing

---

## 7. Market and Competitors (contextual)

| Competitor/Approach | Category | Strengths | Weaknesses | Our differentiator |
|---|---|---|---|---|
| Manual Excel/BI tracking | Traditional | Easy to start | Reactive, slow | ML-based proactive risk prediction |
| Enterprise SCM suites | Commercial | Integrations, scale | Costly/complex | Lightweight, educational, fast prototype |
| Generic ML notebook | Technical | Flexible | Not productized | Web platform + dashboards + deployable |

---

## 8. Objectives and Success Metrics

- **O1 Model utility:** Achieve usable predictive performance on test set  
  - KPI: F1-score (used for best model selection), ROC-AUC  
- **O2 Prediction UX speed:** Complete a prediction submission quickly  
  - KPI: prediction workflow completion time ≤ 60 seconds  
- **O3 App reliability:** Pages load without errors when artifacts exist  
  - KPI: 0 crashes; graceful “setup required” otherwise  
- **O4 Deployment readiness:** Deployable using Render/Gunicorn  
  - KPI: start command `gunicorn app:app` works consistently

---

## 9. Key Features

| Feature | Description | Priority | Dependencies | Acceptance criteria |
|---|---|---:|---|---|
| Dataset generator | Generates synthetic event dataset | Must | numpy/pandas | CSV created in `data/` |
| Training + best model selection | Trains multiple models and selects best by F1 | Must | scikit-learn | Artifacts saved in `model/` |
| Dashboard | Summary metrics + top disruptions | Must | artifacts + CSV | `/` renders charts/tables |
| Prediction + recommendations | Form → probability → risk level → recommendations | Must | model artifacts | `/predict` works end-to-end |
| Model performance view | Compare models, confusion matrix | Should | metrics.json | `/performance` shows metrics |
| Analytics view | Trend charts + aggregate insights | Should | CSV | `/analytics` renders correctly |
| Deployment config | Render/Gunicorn scripts | Must | build.sh | Deploy succeeds |

---

## 10. Architecture

### 10.1 High-level architecture
- **Client/UI:** Server-rendered pages using Flask + Jinja templates (`templates/`)
- **Backend service:** Single Flask app (`app.py`) with routes:
  - `/` dashboard
  - `/predict`
  - `/performance`
  - `/analytics`
- **ML layer:** Offline training pipeline produces inference artifacts
- **Data store:** CSV dataset (`data/supply_chain_events.csv`)
- **Model store:** Local filesystem directory `model/` (pkl + json)

### 10.2 API / Route snapshot

| Route | Method | Purpose | Inputs | Outputs |
|---|---|---|---|---|
| `/` | GET | Dashboard summary | — | HTML dashboard |
| `/predict` | GET/POST | Predict risk | Form fields | HTML result view |
| `/performance` | GET | Compare model metrics | — | HTML metrics view |
| `/analytics` | GET | Trends and aggregates | — | HTML analytics view |

### 10.3 Config and secrets
- Minimal secrets in v1 (no DB credentials)
- Hosting expects `PORT` and optionally `FLASK_DEBUG`

---

## 11. Data Design

### 11.1 Data dictionary (key fields)

| Entity (CSV row) | Field | Type | Notes |
|---|---|---|---|
| Event | `event_id` | string | unique id like EVT-0001 |
| Event | `event_date` | date | synthetic date |
| Event | `event_type` | category | port congestion, supplier delay, etc. |
| Event | `severity_level` | category | Low/Medium/High/Critical |
| Event | `cause` | category | Weather, Transportation, System Failure, etc. |
| Event | `country` | category | USA, India, etc. |
| Event | `financial_impact` | int | 10k–500k synthetic |
| Target | `disruption` | 0/1 | label based on weighted score |

### 11.2 Artifacts produced
- `model/disruption_model.pkl`
- `model/scaler.pkl`
- `model/encoders.pkl`
- `model/features.pkl`
- `model/metrics.json`

---

## 12. Technical Workflow Diagrams (to include in final submission)

1. **Data Flow Diagram (DFD)**  
   generate_data → CSV → train_model → artifacts → Flask app → UI pages

2. **Sequence Diagram (Prediction)**  
   User submits form → Flask parses → encodes/scales → model predicts → UI renders probability + recommendations

3. **ER Diagram**  
   Not applicable in v1 (CSV-based); if extended to DB, include tables: events, predictions, users, audits.

4. **Workflow / Architecture Diagram**  
   Browser ↔ Flask ↔ (CSV + model artifacts)  

---

## 13. Quality: NFRs and Testing

### 13.1 NFR targets
- **Availability:** ≥ 99% (demo target; depends on hosting)
- **Latency:** prediction response < 1s for single request on typical machine
- **Reliability:** setup check prevents runtime crashes when artifacts missing
- **Maintainability:** clear separation between training scripts and app

### 13.2 Test plan (practical v1)
- **Unit tests (optional in v1):**
  - Form parsing defaults
  - Artifact loading (happy-path + missing files)
- **Integration tests:**
  - Run `generate_data.py` then `train_model.py` then start app
  - Validate all 4 routes load successfully
- **UI checks:**
  - Form validation for numeric financial impact
  - Responsiveness on laptop screen

---

## 14. Security and Compliance

### 14.1 Threat model (lightweight)
- **Risk:** Missing/invalid artifacts → app errors  
  - Mitigation: `setup_ready()` + setup_required page
- **Risk:** Input injection via form fields (low risk in demo)  
  - Mitigation: server-side parsing, type casting, limited categories
- **Risk:** Data privacy  
  - In v1 dataset is synthetic → no PII

### 14.2 AuthN/AuthZ
- Not implemented in v1 (single-user demo system)

### 14.3 Logging
- Basic server logs via Gunicorn/Render
- Future: add structured logs for predictions

---

## 15. Delivery and Operations

### 15.1 Release plan
- v1 demo: show data generation → training → web app pages and predictions

### 15.2 CI/CD and rollback (simple)
- Deployment uses:
  - `buildCommand: ./build.sh`
  - `startCommand: gunicorn app:app`
- Rollback: redeploy previous successful build (platform-level)

### 15.3 Monitoring
- Basic uptime and request logs on hosting provider

---

## 16. Risks and Mitigations

| Risk | Probability | Impact | Mitigation | Owner |
|---|---:|---:|---|---|
| Artifacts missing in deployment | Medium | High | Prebuild step or include artifacts; setup page fallback | Rishabh |
| Model performance unstable due to synthetic logic | Medium | Medium | Tune weights/data; report metrics transparently | Rishabh |
| UI pages not consistent | Medium | Medium | UI kit + reusable components | Jaya |
| Backend bugs in encoding/prediction mapping | Medium | High | Validation + integration testing | Ananshi |

---

## 17. Research and Evaluation

- Compare candidate algorithms: Random Forest, Gradient Boosting, Logistic Regression
- Evaluation metrics recorded in `model/metrics.json`
- Best model selected using F1-score (v1 decision rule)

---

## 18. Appendices

### Glossary
- **Disruption:** high-risk supply event predicted to cause breakdown/delay
- **F1-score:** harmonic mean of precision and recall
- **ROC-AUC:** ranking quality metric for classifiers
- **Artifacts:** saved model + preprocessing objects used for inference

### References
- scikit-learn documentation
- Flask documentation
- Project repository README and source code
