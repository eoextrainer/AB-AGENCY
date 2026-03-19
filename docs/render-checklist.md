# Render Healthcheck And Environment Checklist

Use this checklist before and after each Render deployment.

## Environment Checklist

### Backend

Set these variables on the Render backend service:

1. `DATABASE_URL`
2. `SECRET_KEY`
3. `ENVIRONMENT=production`
4. `FIRST_SUPERUSER_EMAIL`
5. `FIRST_SUPERUSER_USERNAME`
6. `FIRST_SUPERUSER_PASSWORD`
7. `ARTIST_AMBRE_PASSWORD`
8. `ARTIST_CELESTE_PASSWORD`
9. `ARTIST_SANTIAGO_PASSWORD`
10. `CORS_ORIGINS`
11. `CMS_PROJECT_ID`
12. `CMS_DATASET`
13. `CMS_API_VERSION`

Production rule:
The backend will now refuse to boot in `production` if any of these passwords are left on the default dev values:

1. `FIRST_SUPERUSER_PASSWORD=admin123`
2. `ARTIST_AMBRE_PASSWORD=pass123`
3. `ARTIST_CELESTE_PASSWORD=pass123`
4. `ARTIST_SANTIAGO_PASSWORD=pass123`

### Frontend

Set these variables on the Render frontend service:

1. `NEXT_PUBLIC_API_BASE_URL`
2. `NEXT_SERVER_API_BASE_URL`
3. `NEXT_PUBLIC_SANITY_PROJECT_ID`
4. `NEXT_PUBLIC_SANITY_DATASET`
5. `NEXT_PUBLIC_SANITY_API_VERSION`
6. `ADMIN_API_USERNAME`
7. `ADMIN_API_PASSWORD`
8. `NEXT_PUBLIC_SHOW_DEMO_CREDENTIALS=false`

## Render Healthcheck Paths

The Render blueprint now defines these healthcheck paths:

1. Backend: `/health`
2. Frontend: `/`

## Post-Deploy Healthcheck Steps

1. Confirm the backend service is healthy in Render.
2. Open `https://YOUR-BACKEND-URL/health`.
3. Confirm the response is `{"status":"ok"}`.
4. Open `https://YOUR-FRONTEND-URL/`.
5. Open `https://YOUR-FRONTEND-URL/login`.
6. Confirm the login page loads and the demo credential drawer is hidden in production.
7. Open `https://YOUR-BACKEND-URL/api/public/homepage`.
8. Confirm seeded homepage data is returned.
9. Open `https://YOUR-BACKEND-URL/api/artists`.
10. Confirm seeded artists and media assets are returned.

## Fast Verification Script

Run [scripts/render_healthcheck.sh](../scripts/render_healthcheck.sh) after deployment:

```bash
./scripts/render_healthcheck.sh https://YOUR-FRONTEND-URL https://YOUR-BACKEND-URL
```
