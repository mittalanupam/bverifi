# Railway Deployment Guide (Easiest Option)

Deploy **bverifi** (Django + React + PostgreSQL) on [Railway](https://railway.com) with minimal config. Railway handles networking, SSL, and scaling.

## Why Railway?

- Zero-config deploys; [Railway](https://railway.com) reads your code and sets the right settings.
- Free tier ($5 credit/month); hard spending limits available.
- Auto-deploys on git push; previews per PR.
- Managed PostgreSQL; backend supports `DATABASE_URL` for one-click DB.

## Prerequisites

1. **Code on GitHub** – Push this repo to a GitHub repository.
2. **Railway account** – Sign up at [railway.app](https://railway.app) with GitHub.

---

## Step-by-Step Guide

### Step 1: Create a New Project

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project**.
3. Choose **Deploy from GitHub repo** and select your **bverifi** repository.
4. Do **not** deploy the root yet; we will add three services (Postgres, backend, frontend).

### Step 2: Add PostgreSQL

1. In the project, click **+ New**.
2. Select **Database** → **PostgreSQL**.
3. Railway creates a Postgres service and exposes variables (e.g. `DATABASE_URL`, `PGHOST`, etc.).
4. Open the Postgres service → **Variables** and note that `DATABASE_URL` is set (backend will use it automatically).

### Step 3: Deploy the Backend (Django)

1. Click **+ New** → **GitHub Repo** and select the same bverifi repo.
2. In the new service:
   - **Settings** → **Root Directory**: set to `backend`.
   - **Settings** → **Builder**: choose **Dockerfile** and set **Dockerfile Path** to `Dockerfile.prod` (or leave default if it picks `Dockerfile.prod`).
3. **Variables** → add (or use **Variables** from Postgres and reference them):

| Variable | Value |
|----------|--------|
| `DEBUG` | `False` |
| `SECRET_KEY` | A long random string (e.g. from `openssl rand -hex 32`) |
| `ALLOWED_HOSTS` | `*` or `*.railway.app` |
| `DATABASE_URL` | **Reference**: click “Add variable” → “Add reference” → choose your **Postgres** service → `DATABASE_URL`. (If you prefer separate vars: `DATABASE_HOST`, `DATABASE_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` from Postgres.) |
| `CORS_ALLOWED_ORIGINS` | Leave empty for now; after frontend is deployed, set to your frontend URL (e.g. `https://your-frontend.up.railway.app`). |

4. **Connect Postgres to Backend**: In the backend service, **Variables** → add reference to Postgres `DATABASE_URL` so the backend uses Railway’s Postgres.
5. Deploy: Railway will build from `backend/Dockerfile.prod` and run Gunicorn on `$PORT`.

After the first deploy, open the backend service → **Settings** → **Networking** → **Generate domain** to get the backend URL (e.g. `https://backend-xxx.up.railway.app`).

### Step 4: Deploy the Frontend (React)

1. Click **+ New** → **GitHub Repo** and select the same bverifi repo.
2. In the new service:
   - **Settings** → **Root Directory**: set to `frontend`.
   - **Settings** → **Builder**: **Nixpacks** (default; do not use Docker so Railway can inject `PORT`).
   - **Settings** → **Deploy** → **Start Command** (optional): `npm run start:prod` (or rely on `frontend/railway.toml` which already sets this).
3. **Variables** → add:

| Variable | Value |
|----------|--------|
| `REACT_APP_API_URL` | Your backend API URL, e.g. `https://backend-xxx.up.railway.app/api` (use the URL from Step 3). |

4. Deploy: Railway runs `npm install`, `npm run build`, then `npm run start:prod` (serves `build` on `$PORT`).

Generate a public domain for the frontend under **Settings** → **Networking** → **Generate domain**.

### Step 5: Update CORS and API URL

1. **Backend** → **Variables**: set `CORS_ALLOWED_ORIGINS` to your frontend URL (e.g. `https://frontend-xxx.up.railway.app`). Redeploy if needed.
2. **Frontend** → **Variables**: ensure `REACT_APP_API_URL` is exactly your backend URL + `/api`. Redeploy so the build gets the correct API URL.

### Step 6: Run Migrations and Create Superuser

Use the Railway CLI (run in a terminal, from your machine):

```bash
# Install CLI
npm i -g @railway/cli

# Login (opens browser)
railway login

# Link to your project and backend service
railway link
# Select your project and the backend service

# Run migrations
railway run python manage.py migrate

# Create Django admin user
railway run python manage.py createsuperuser
```

### Step 7: Access the App

- **Frontend**: `https://<frontend-service>.up.railway.app`
- **Backend API**: `https://<backend-service>.up.railway.app/api/`
- **Django Admin**: `https://<backend-service>.up.railway.app/admin/`

---

## Environment Variables Reference

### Backend (Django)

| Variable | Required | Description |
|----------|----------|-------------|
| `DEBUG` | Yes | `False` in production |
| `SECRET_KEY` | Yes | Long random secret |
| `ALLOWED_HOSTS` | Yes | `*` or `*.railway.app` |
| `DATABASE_URL` | Yes (recommended) | From Postgres service reference (one-click) |
| `CORS_ALLOWED_ORIGINS` | Yes | Frontend URL (comma-separated if multiple) |

If you don’t use `DATABASE_URL`, set: `DATABASE_HOST`, `DATABASE_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (from Postgres service).

### Frontend (React)

| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_API_URL` | Yes | Backend base URL + `/api` (e.g. `https://backend-xxx.up.railway.app/api`) |

## Railway CLI Commands

```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Link project (select project + backend service)
railway link

# View logs
railway logs

# Run commands (from repo root; backend must be linked)
railway run python manage.py migrate
railway run python manage.py createsuperuser

# Open shell in backend container
railway shell
```

## Pricing

- **Free Tier**: $5 credit/month ([railway.com/pricing](https://railway.com/pricing))
- **Hobby / Pro**: Pay-as-you-go; hard spending limits available

## Tips

1. **Variable references**: In Variables, use “Add reference” to pull `DATABASE_URL` from the Postgres service.
2. **Auto-deploy**: Every git push to the connected branch triggers a new deploy.
3. **Logs & metrics**: Use the Railway dashboard for logs and resource usage.
4. **Custom domain**: **Settings** → **Networking** → add a custom domain and update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`.

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| **Backend build fails** | Build logs; ensure `backend/Dockerfile.prod` and `backend/requirements.txt` are correct. |
| **Database connection** | Backend has `DATABASE_URL` (or all Postgres vars) and Postgres service is running. |
| **CORS errors** | `CORS_ALLOWED_ORIGINS` includes the exact frontend URL (no trailing slash). |
| **Frontend wrong API** | `REACT_APP_API_URL` is set and frontend was **rebuilt** after changing it. |

## Support

- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)



