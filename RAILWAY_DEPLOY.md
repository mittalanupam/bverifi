# Railway Deployment Guide (Easiest Option)

Railway is the easiest way to deploy your application without managing servers.

## Why Railway?

- ✅ Zero configuration
- ✅ Free tier available
- ✅ Auto-deploys on git push
- ✅ Free SSL certificate
- ✅ Handles Docker automatically
- ✅ Managed PostgreSQL available

## Step-by-Step Guide

### Step 1: Prepare Your Repository

1. Make sure your code is on GitHub
2. Ensure these files exist:
   - `docker-compose.prod.yml`
   - `.env.example`
   - `backend/Dockerfile.prod`
   - `frontend/Dockerfile.prod`

### Step 2: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub
4. Authorize Railway to access your repositories

### Step 3: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will detect your Docker setup

### Step 4: Add PostgreSQL Database

1. In your project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway creates a managed PostgreSQL instance
4. Note the connection details (you'll need them)

### Step 5: Configure Backend Service

1. Railway should auto-detect your backend
2. If not, click "New" → "GitHub Repo" → select your repo
3. Set root directory: `backend`
4. Add environment variables:

```
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=*.railway.app,yourdomain.com
DATABASE_HOST=${{Postgres.PGHOST}}
DATABASE_PORT=${{Postgres.PGPORT}}
POSTGRES_DB=${{Postgres.PGDATABASE}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
CORS_ALLOWED_ORIGINS=https://your-app.railway.app
```

5. Set build command (if needed):
   - Build: `docker build -f Dockerfile.prod -t backend .`
   - Start: `gunicorn --bind 0.0.0.0:$PORT --workers 4 backend.wsgi:application`

### Step 6: Configure Frontend Service

1. Click "New" → "GitHub Repo" → select your repo
2. Set root directory: `frontend`
3. Add environment variables:

```
REACT_APP_API_URL=https://your-backend.railway.app/api
```

4. Set build command:
   - Build: `npm run build`
   - Start: `serve -s build -l 3000`

### Step 7: Set Up Custom Domain (Optional)

1. Go to your service settings
2. Click "Settings" → "Networking"
3. Add custom domain
4. Railway provides DNS instructions
5. Update CORS_ALLOWED_ORIGINS with your domain

### Step 8: Run Migrations

1. Go to backend service
2. Click "Deployments" → "View Logs"
3. Or use Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

### Step 9: Access Your Application

Railway provides URLs like:
- Frontend: `https://your-app.railway.app`
- Backend: `https://your-backend.railway.app`
- Admin: `https://your-backend.railway.app/admin/`

## Environment Variables Reference

### Backend Variables:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*.railway.app,yourdomain.com
DATABASE_HOST=${{Postgres.PGHOST}}
DATABASE_PORT=${{Postgres.PGPORT}}
POSTGRES_DB=${{Postgres.PGDATABASE}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
CORS_ALLOWED_ORIGINS=https://your-frontend.railway.app
```

### Frontend Variables:
```
REACT_APP_API_URL=https://your-backend.railway.app/api
```

## Railway CLI Commands

```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser

# Open shell
railway shell
```

## Pricing

- **Free Tier**: $5 credit/month
- **Hobby Plan**: $5/month (if you exceed free tier)
- **Pro Plan**: $20/month (for production)

## Tips

1. **Use Railway Variables**: Reference other services using `${{Service.Variable}}`
2. **Auto-Deploy**: Railway auto-deploys on every git push
3. **Logs**: View real-time logs in Railway dashboard
4. **Metrics**: Monitor usage in Railway dashboard
5. **Backups**: Railway handles database backups automatically

## Troubleshooting

### Build Fails:
- Check build logs in Railway dashboard
- Verify Dockerfile paths
- Ensure all dependencies are in requirements.txt

### Database Connection Issues:
- Verify environment variables reference Postgres service correctly
- Check database is running
- Verify credentials

### CORS Errors:
- Update CORS_ALLOWED_ORIGINS with Railway URLs
- Check frontend API_URL matches backend URL

## Next Steps

1. Set up custom domain
2. Configure monitoring
3. Set up CI/CD (already done with Railway!)
4. Add more services as needed

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app


