# Quick Deployment Guide

## 🚀 Fastest Way to Deploy

### Step 1: Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and set your production values:
- Generate a secret key: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- Set a strong database password
- Add your domain to ALLOWED_HOSTS

### Step 2: Deploy

```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d --build
```

### Step 3: Create Admin User

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### Step 4: Access Your App

- Frontend: http://yourdomain.com (or http://localhost)
- Admin: http://yourdomain.com/admin/
- API: http://yourdomain.com/api/

## 📝 Example .env File

```env
POSTGRES_DB=ankur_db
POSTGRES_USER=ankur_user
POSTGRES_PASSWORD=YourStrongPassword123!

SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

FRONTEND_PORT=80
REACT_APP_API_URL=http://yourdomain.com/api
CORS_ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com
```

## 🔧 Common Commands

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Update and redeploy
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📚 Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment options and best practices.


