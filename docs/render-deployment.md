# Render Deployment Guide

This project deploys cleanly to Render as three resources:

1. A PostgreSQL database
2. A Python web service for the FastAPI backend
3. A Node web service for the Next.js frontend

The backend already handles two critical deployment tasks at startup:

- it runs database migrations when started with `alembic upgrade head`
- it seeds and upserts the default admin user, artist users, artist profiles, services, and media inside `app.main.seed_database`

That means the remote database is seeded automatically the first time the backend boots successfully.

## Prerequisites

1. Push the repository to GitHub
2. Have a Render account connected to the GitHub repository
3. Decide the production admin password you want to use for `FIRST_SUPERUSER_PASSWORD`

## Recommended Deployment Shape

Create these Render resources:

1. `ab-agency-db` as a PostgreSQL database
2. `ab-agency-backend` as a Python web service rooted at `backend`
3. `ab-agency-frontend` as a Node web service rooted at `frontend`

This repository includes [render.yaml](../render.yaml) to predefine that layout.

## Option A: Deploy With render.yaml

1. In Render, click New and choose Blueprint.
2. Select the `eoextrainer/AB-AGENCY` repository.
3. Render will detect [render.yaml](../render.yaml).
4. Continue the setup and create the stack.
5. When prompted for manual environment values, provide these:
   - `FIRST_SUPERUSER_PASSWORD`: choose a strong production password
   - `ARTIST_AMBRE_PASSWORD`: choose a strong artist password for Ambre
   - `ARTIST_CELESTE_PASSWORD`: choose a strong artist password for Celeste
   - `ARTIST_SANTIAGO_PASSWORD`: choose a strong artist password for Santiago
   - `ADMIN_API_PASSWORD`: set it to the same value as `FIRST_SUPERUSER_PASSWORD`
   - `CORS_ORIGINS`: use a JSON array containing your frontend origin, for example `["https://ab-agency-frontend.onrender.com"]`
   - `NEXT_PUBLIC_API_BASE_URL`: set to your backend public API URL, for example `https://ab-agency-backend.onrender.com/api`
   - `NEXT_SERVER_API_BASE_URL`: set to the same backend public API URL, for example `https://ab-agency-backend.onrender.com/api`
   - `NEXT_PUBLIC_SHOW_DEMO_CREDENTIALS`: set this to `false`
6. Deploy the blueprint.

## Option B: Create Services Manually

If you prefer to configure each service in the UI, use the steps below.

### 1. Create the PostgreSQL database

1. In Render, click New and choose PostgreSQL.
2. Name it `ab-agency-db`.
3. Set database name to `ab_agency`.
4. Set user to `ab_agency`.
5. Create the database.
6. After creation, copy the Internal Database URL.

Note:
The backend accepts a standard PostgreSQL SQLAlchemy URL. Render usually provides a URL like `postgresql://...`, which works with the dependencies in this project.

### 2. Create the backend web service

1. In Render, click New and choose Web Service.
2. Connect the GitHub repository.
3. Set Name to `ab-agency-backend`.
4. Set Root Directory to `backend`.
5. Set Runtime to Python 3.
6. Set Build Command to:

```bash
pip install --no-cache-dir -r requirements.txt
```

1. Set Start Command to:

```bash
bash -lc 'alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT}'
```

1. Add these environment variables:
   - `DATABASE_URL`: paste the database Internal Database URL
   - `SECRET_KEY`: generate a long random secret
   - `ENVIRONMENT`: `production`
   - `FIRST_SUPERUSER_EMAIL`: `admin@ab-agency.com`
   - `FIRST_SUPERUSER_USERNAME`: `admin`
   - `FIRST_SUPERUSER_PASSWORD`: your chosen production password
   - `ARTIST_AMBRE_PASSWORD`: your production artist password for Ambre
   - `ARTIST_CELESTE_PASSWORD`: your production artist password for Celeste
   - `ARTIST_SANTIAGO_PASSWORD`: your production artist password for Santiago
   - `CORS_ORIGINS`: JSON array containing the frontend origin, for example `["https://ab-agency-frontend.onrender.com"]`
   - `CMS_PROJECT_ID`: `replace-me` unless you have a real Sanity project
   - `CMS_DATASET`: `production`
   - `CMS_API_VERSION`: `2025-01-01`
1. Deploy the backend.

What happens on first backend startup:

1. `alembic upgrade head` applies migrations to the remote database
2. FastAPI starts
3. `seed_database()` runs during app startup
4. the admin user and seeded artists are inserted or updated

### 3. Create the frontend web service

1. In Render, click New and choose Web Service.
2. Connect the same repository.
3. Set Name to `ab-agency-frontend`.
4. Set Root Directory to `frontend`.
5. Set Runtime to Node.
6. Set Build Command to:

```bash
npm install && npm run build
```

1. Set Start Command to:

```bash
npx next start -H 0.0.0.0 -p ${PORT}
```

1. Add these environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: `https://YOUR-BACKEND-URL/api`
   - `NEXT_SERVER_API_BASE_URL`: `https://YOUR-BACKEND-URL/api`
   - `NEXT_PUBLIC_SANITY_PROJECT_ID`: `replace-me`
   - `NEXT_PUBLIC_SANITY_DATASET`: `production`
   - `NEXT_PUBLIC_SANITY_API_VERSION`: `2025-01-01`
   - `ADMIN_API_USERNAME`: `admin`
   - `ADMIN_API_PASSWORD`: same value as `FIRST_SUPERUSER_PASSWORD`
   - `NEXT_PUBLIC_SHOW_DEMO_CREDENTIALS`: `false`
1. Deploy the frontend.

Important:
Do not use the existing frontend Dockerfile directly on Render for production. It currently starts `npm run dev`, which is suitable for local development, not production hosting.

## How Remote Database Seeding Works

You asked specifically about seeding the remote database. In this codebase, seeding is automatic.

The seed flow lives in [backend/app/main.py](../backend/app/main.py) and is executed every time the backend starts. It uses upsert-style logic:

- seeded artists are created if missing
- existing seeded artists are updated if they already exist
- media assets for seeded artists are refreshed
- seeded users are created or updated
- service pages are created or updated

That means the normal deployment flow is enough to seed the remote database.

## How To Force a Reseed Later

If you change the seed data and want Render to apply it again:

1. Commit and push the updated backend code
2. Trigger a new deploy for `ab-agency-backend`
3. Wait for the backend service to restart

On startup, the backend will run the seed logic again and upsert the records.

If you need a completely clean database instead of an upsert:

1. Create a fresh Render PostgreSQL database
2. Point `DATABASE_URL` to the new database
3. Redeploy the backend

That gives you a clean first-run seed.

## Post-Deployment Verification

After deployment, verify in this order:

1. Open `https://YOUR-BACKEND-URL/health` and confirm it returns `{"status":"ok"}`
2. Open `https://YOUR-FRONTEND-URL`
3. Confirm the homepage loads in French
4. Confirm artist video tiles render
5. Log in with the admin credentials you configured
6. Open the admin page and confirm dashboard data loads
7. Log in with an artist account and confirm the artist portal loads

## Seeded Accounts After Deployment

If you keep the current seed behavior, the following accounts will exist remotely after the backend boots:

1. Admin user:
   - username: `admin`
   - password: value from `FIRST_SUPERUSER_PASSWORD`
2. Artist users:
   - `ambre / value from ARTIST_AMBRE_PASSWORD`
   - `celeste / value from ARTIST_CELESTE_PASSWORD`
   - `santiago / value from ARTIST_SANTIAGO_PASSWORD`

The backend now refuses to boot in production if any seeded password is left on the default demo value.

## Common Render-Specific Notes

1. If the frontend cannot reach the backend, check `NEXT_PUBLIC_API_BASE_URL` and `NEXT_SERVER_API_BASE_URL` first.
2. If login works locally but not on Render, verify `ADMIN_API_PASSWORD` matches `FIRST_SUPERUSER_PASSWORD`.
3. If browser API calls are blocked, the `CORS_ORIGINS` JSON string is probably wrong.
4. If the backend fails during startup, inspect the logs for migration or database connection errors.
5. If you want zero ambiguity, use the backend public Render URL for both frontend API variables.

## Recommended First Production Hardening

Before a public launch, make these changes:

1. set unique strong values for all seeded user passwords in Render
2. replace `replace-me` CMS values if Sanity will be used
3. set a strong `SECRET_KEY`
4. restrict `CORS_ORIGINS` to the exact production frontend URL
5. remove or change any demo-only credentials you do not want in production
6. run the Render verification checklist in [render-checklist.md](./render-checklist.md)
