# marshall-app — working notes

Snapshot so we can pick up cleanly next session. Living doc — update as state changes.

## What this is

`marshall-app` is the working implementation of [marshall.us](https://marshall.us/) — buyer-side intake + readiness-scored manufacturer database aligned with the site's positioning ("Find production-ready manufacturers faster", Need → Match → Verify → Route).

- Repo: https://github.com/gheniabla/marshall-app  *(public)*
- Live: https://marshall-app.onrender.com
- Local working dir: `/Users/abla/Desktop/Marshall`
- Branch: `main`

## Stack

- **Backend**: FastAPI — `backend/app.py`
- **DB**: SQLAlchemy. SQLite locally, Neon Postgres in prod via `DATABASE_URL`
- **Frontend**: single-file `frontend/index.html` served by FastAPI
- **Seed data**: `scripts/scrape_defense_companies.py` (curated, in-memory, ~100 SoCal defense manufacturers — no external HTTP)
- **Hosting**: Render free web service (sleeps after 15 min idle), Neon free Postgres

## Deployment wiring

`render.yaml` is a Blueprint. Three env vars must be set in the Render dashboard (none synced from yaml):

| Env var      | What                                                              |
|--------------|-------------------------------------------------------------------|
| `DATABASE_URL` | Neon connection string (Render auto-rewrites `postgresql://` → `postgresql+psycopg://` driver in `database/models.py`). |
| `ADMIN_USER` | username for HTTP Basic gate on write endpoints.                  |
| `ADMIN_PASS` | matching password.                                                 |

User chose `marshall37` / `20212023` at last check — re-confirm at runtime, do **not** assume.

If the app boots but writes return 401 with the user's chosen creds → env vars weren't actually saved/redeployed. Verify with:
```
curl -i -u "$ADMIN_USER:$ADMIN_PASS" -X POST https://marshall-app.onrender.com/api/companies \
  -H 'Content-Type: application/json' -d '{"company_name":"AuthProbe","location":"X, CA"}'
```

## Auth design (agreed)

- **Public reads**: GET companies/search/stats, GET/POST `/api/needs` (buyer funnel — must stay frictionless)
- **Admin-gated writes**: `POST/PUT/DELETE /api/companies*`, `POST /api/companies/{id}/readiness`
- HTTP Basic with constant-time compare in `require_admin`. Default fallback `admin`/`changeme` logs a warning so unset env vars are obvious.
- Frontend: `getAdminAuth()` prompts on `+ Add Company` *click* (not on submit), caches in `sessionStorage`. `adminFetch()` retries once on 401 (re-prompt). "Admin sign out" button in header clears the cache.

## Data model touch points

`database/models.py`:
- `Company` — added activation signals: `active_capacity_status`, `lead_time_days`, `itar_registered`, `cmmc_level`.
- `ReadinessScore` — added `mrl_level` (1–10). `calculate_overall_score()` now treats `0` as **unassessed** and averages only the assessed pillars.
- `ManufacturingNeed` — buyer intake (`submitted` → `matched` → `verified` → `routed`).

`backend/app.py`:
- Split into `ReadinessScoreSchema` (response, all defaults) and `ReadinessScoreUpdateSchema` (request, all `Optional[None]`). Update handler uses `dict(exclude_unset=True)` so partial writes don't zero out unset pillars.
- New endpoints: `POST /api/needs`, `GET /api/needs`, `POST /api/needs/{id}/match`.
- Startup hook: auto-seeds an empty DB; then **recomputes overall_readiness_score for every row** under the current rule (cheap, self-heals stale data). Disable seeding with `AUTO_SEED=0`.

## Known sharp edges / open items

- **Render free dyno cold start** — first request after 15 min idle is slow (~30 s). Acceptable for demo.
- **Author email in git history** — every commit so far carries `gheni.abla@gmail.com`. Repo is public. User has not asked to scrub via `git filter-repo` + force-push. If they bring this up, that's the path; otherwise leave it.
- **Frontend score modal UX** — score entry is a `prompt()` chain (commas-separated). Functional; not pretty. Not a priority unless asked.
- **No tests yet.** Adding pytest + a few API smoke tests would be cheap. Not requested.
- **Neon free tier auto-suspends** an idle Postgres branch — first query after suspend has a couple-second cold start. Adds to Render's own cold start.
- **`raw-material/`** holds founder docs, decks, original site export. Gitignored. Do **not** check it in.

## Recent timeline (most recent first)

- `a1d76f8` Fix readiness scoring: ignore 0 pillars, partial updates, recalc on boot
- `e03b7b2` Fix "Error loading companies" + admin sign-out button
- `40cffcd` Prompt for admin creds on Add Company click
- `ddad636` Gate writes with HTTP Basic admin auth
- `dae0b26` Auto-seed empty DB on startup
- `fe7d8d6` Force psycopg v3 driver for Neon `postgresql://` URLs
- `bce54ae` Render + Neon deployment scaffolding
- `f77633a` Initial commit (FastAPI + readiness model + frontend, raw-material excluded)

## Likely next-session prompts to anticipate

- "Why did Render deploy fail" → check Render logs; check that `DATABASE_URL` / `ADMIN_*` are saved on the *correct* service.
- "Add field X to company" → model + Pydantic schemas (both `CompanySchema` and create/update) + frontend modal.
- "Make scoring UI nicer" → replace the prompt chain in `openScoreModal` with a real form modal mirroring `addCompanyModal`.
- "Add pytest" → fixture that seeds a temp SQLite DB with `AUTO_SEED=0`; client uses `httpx.AsyncClient(app=app)`.
- "Move off Render" → Fly.io (`fly.toml` + Dockerfile, persistent volume, no separate DB needed) is the cleanest swap.

## Verification snippets

```bash
# health + content sanity
curl -s https://marshall-app.onrender.com/health
curl -s "https://marshall-app.onrender.com/api/stats" | python3 -m json.tool | head
curl -s "https://marshall-app.onrender.com/api/companies?limit=2" | python3 -m json.tool | head -40

# auth probe (replace user:pass with the actual ADMIN_USER / ADMIN_PASS)
curl -i -u user:pass -X POST https://marshall-app.onrender.com/api/companies \
  -H 'Content-Type: application/json' \
  -d '{"company_name":"AuthProbe","location":"Los Angeles, CA"}'
```
