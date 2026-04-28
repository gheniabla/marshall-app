# Deploy marshall-app (free)

Render (web service) + Neon (Postgres). Both free tiers, no credit card.

## 1. Provision Postgres on Neon

1. Sign up at https://neon.tech with GitHub.
2. Create project → name it `marshall-app`. Region: pick the same region you'll deploy Render to (e.g. US West / Oregon).
3. Copy the **connection string** from the dashboard. It looks like:
   `postgresql://user:pass@ep-xxxx.us-west-2.aws.neon.tech/neondb?sslmode=require`

## 2. Deploy on Render

1. Sign up at https://render.com with GitHub.
2. **New → Blueprint** → pick the `gheniabla/marshall-app` repo. Render reads `render.yaml`.
3. When prompted for `DATABASE_URL`, paste the Neon connection string from step 1.
4. Click **Apply**. First build takes ~3 minutes.

## 3. Seed the database (one time)

From your laptop, point the seed script at Neon:

```bash
export DATABASE_URL='postgresql://user:pass@ep-xxxx.us-west-2.aws.neon.tech/neondb?sslmode=require'
python scripts/populate_db.py --action populate
python scripts/populate_db.py --action add-scores
```

Or run the same commands from Render's Shell tab.

## 4. Visit your app

Render gives you `https://marshall-app.onrender.com` (or similar). API docs at `/docs`.

## Notes / caveats

- **Cold starts**: Render free web services sleep after 15 min of inactivity. First request after sleep takes ~30 s.
- **No persistent disk needed**: state lives in Neon, so redeploys don't wipe data.
- **Auto-deploy**: every push to `main` triggers a redeploy.
- **Custom domain**: free on both Render and Neon. Add it from the Render dashboard.

## Local development still works

The app falls back to local SQLite (`marshall_defense.db`) when `DATABASE_URL` is unset, so nothing changes locally.
