# Marshall — marshall-app

> Find production-ready manufacturers faster.

Marshall helps defense and aerospace buyers **identify, verify, and activate** manufacturers based on real readiness — certifications, capacity, and fit — not directory listings.

This repo (`marshall-app`) is the working implementation of the Marshall platform: a buyer-side intake, a readiness-scored manufacturer database, and a match → verify → route pipeline aligned with [marshall.us](https://marshall.us/).

## The bottleneck Marshall addresses

> The bottleneck is not supplier discovery. It is supplier **activation**.

Buyers submit a structured manufacturing need. Marshall scores and ranks the network on readiness, verifies certifications and capacity, and routes a qualified shortlist — not a referral list.

## Pipeline

```
Need  →  Match  →  Verify  →  Route
```

| Step | What happens | Where in the app |
|------|--------------|------------------|
| **01 / Submit** | Buyer submits need: part, process, material, quantity, urgency, certifications, geography, constraints. | `POST /api/needs` |
| **02 / Score** | Manufacturers ranked on MRL, active capacity, certification status, and fit against the requirement. | `POST /api/needs/{id}/match` |
| **03 / Verify** | Certifications, lead time, and active capacity confirmed before the shortlist is shared. | `active_capacity_status`, `cmmc_level`, `itar_registered`, `lead_time_days` on `Company` |
| **04 / Route** | Marshall manages the introduction — structured, tracked, outcome-oriented. | `relationship_status` lifecycle on `Company` (`cold` → `warm` → `engaged` → `partner`) |

## Why Marshall

- **Readiness-first matching** — every manufacturer scored on Manufacturing Readiness Level (MRL 1–10), active capacity, and certifications. Not just historical capabilities.
- **Verified certifications** — AS9100D, Nadcap, CMMC, ITAR status confirmed and date-stamped. No self-reported data.
- **Constraint intelligence** — geography, security clearance, tooling, and lead-time constraints surface in every match.
- **Production bridge** — Marshall manages the handoff from shortlist to introduction.
- **Defense-native** — built for buyers who operate under real urgency, security, compliance, and volume constraints.

## Architecture

- **Backend**: FastAPI (Python) — `backend/app.py`
- **Database**: SQLite via SQLAlchemy — `database/models.py`
- **Frontend**: HTML / CSS / JS single-page UI — `frontend/index.html`
- **Data ingest**: scrapers and seeders — `scripts/`

### Schema (high level)

`Company`
- Profile: `company_name`, `location`, `state`, `website`, `phone`, `contact_*`
- Capability: `industry_focus`, `manufacturing_processes`, `equipment_capabilities`, `materials`, `certifications`
- Activation signals: `active_capacity_status`, `lead_time_days`, `itar_registered`, `cmmc_level`
- Status: `production_stage`, `relationship_status`, `is_southern_california`

`ReadinessScore` (0–100 unless noted)
- `manufacturing_maturity`
- `quality_compliance_readiness`
- `production_scalability`
- `defense_applicability`
- `responsiveness_operational_readiness`
- `mrl_level` *(1–10, DoD MRL scale)*
- `overall_readiness_score` *(average)*

`ManufacturingNeed` — buyer intake (`submitted` → `matched` → `verified` → `routed`)

## Quick start

```bash
pip install -r requirements.txt
python setup_and_run.py
```

Then open:
- Web UI — http://localhost:8000
- API docs — http://localhost:8000/docs

### Manual

```bash
pip install -r requirements.txt
python scripts/populate_db.py --action populate
python scripts/populate_db.py --action add-scores
cd backend && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API surface

Manufacturers
- `GET    /api/companies` — list (paginated, filterable)
- `GET    /api/companies/search?q=` — search across name, location, certs, capabilities
- `GET    /api/companies/{id}` — detail
- `POST   /api/companies` — create
- `PUT    /api/companies/{id}` — update
- `DELETE /api/companies/{id}` — delete
- `GET    /api/companies/filter/by-readiness?min_score=75` — readiness-ranked

Readiness
- `POST   /api/companies/{id}/readiness` — set/refresh score (incl. `mrl_level`)

Needs (intake / match)
- `POST   /api/needs` — submit a manufacturing need
- `GET    /api/needs?status=submitted` — list needs
- `POST   /api/needs/{id}/match?top_n=5` — return readiness-ranked shortlist

Stats
- `GET    /api/stats` — totals, SoCal count, average readiness, top 5

## Coverage focus

Curated manufacturers across U.S. defense/aerospace clusters, with deep coverage of Southern California (San Diego, Los Angeles, Orange, Ventura, Riverside).

## Production hardening (not yet done)

- Auth (JWT/OAuth2), HTTPS, rate limiting, CORS lock-down
- PostgreSQL in place of SQLite for multi-user
- Background verification jobs for cert/capacity refresh
- Audit log for routed introductions

## Repo layout

```
marshall-app/
├── backend/        FastAPI app
├── database/       SQLAlchemy models
├── frontend/       Web UI
├── scripts/        Scrapers + DB seeders
├── requirements.txt
├── setup_and_run.py
└── README.md
```

`raw-material/` (founder docs, decks, original site export) is intentionally **not** checked in — see `.gitignore`.
