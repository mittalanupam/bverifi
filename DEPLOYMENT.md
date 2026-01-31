# Deployment Guide for Ankur Application

This guide covers deploying the Ankur application to production.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (optional, for production)
- SSL certificate (optional, for HTTPS)

## Quick Start - Production Deployment

### 1. Create Environment File

Copy the example environment file and update with your production values:

```bash
cp .env.example .env
```

Edit `.env` and set:
- Strong `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- Strong `POSTGRES_PASSWORD`
- Your domain in `ALLOWED_HOSTS`
- Update `REACT_APP_API_URL` to match your domain

### 2. Build and Start Production Containers

```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d --build
```

### 3. Create Superuser

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 4. Access Your Application

- **Frontend**: http://yourdomain.com (or http://localhost if using default port)
- **Backend API**: http://yourdomain.com/api/
- **Django Admin**: http://yourdomain.com/admin/

## Deployment Options

### Option 1: Docker Compose on VPS/Server

**Best for**: Single server deployments, small to medium scale

1. **On your server**, clone the repository:
```bash
git clone <your-repo-url>
cd ankur
```

2. **Set up environment**:
```bash
cp .env.example .env
nano .env  # Edit with your values
```

3. **Deploy**:
```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d --build
```

4. **Set up reverse proxy** (Nginx on host):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Cloud Platforms

#### AWS (EC2 + ECS or EC2 with Docker)

1. Launch EC2 instance
2. Install Docker and Docker Compose
3. Follow Option 1 steps
4. Configure security groups to allow HTTP/HTTPS traffic

#### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure build settings:
   - Backend: Python 3.11, build command: `pip install -r requirements.txt`
   - Frontend: Node.js 20, build command: `npm run build`
3. Set environment variables
4. Deploy

#### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```
3. Deploy:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql
git push heroku main
```

#### Railway

1. Connect GitHub repository
2. Railway auto-detects Docker
3. Set environment variables
4. Deploy

### Option 3: Kubernetes

For Kubernetes deployment, you'll need:
- Kubernetes cluster
- Helm charts (can be created)
- Ingress controller

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Use strong database password
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up SSL/HTTPS (Let's Encrypt recommended)
- [ ] Configure database backups
- [ ] Set up monitoring/logging
- [ ] Configure firewall rules
- [ ] Set up regular security updates
- [ ] Create admin user
- [ ] Test all endpoints
- [ ] Set up CI/CD pipeline (optional)

## SSL/HTTPS Setup

### Using Let's Encrypt with Nginx

1. Install Certbot:
```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

2. Get certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. Auto-renewal is set up automatically

## Database Backups

### Manual Backup
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup_$(date +%Y%m%d).sql
```

### Automated Backups (Cron)
Add to crontab:
```bash
0 2 * * * cd /path/to/ankur && docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ankur_user ankur_db > /backups/ankur_$(date +\%Y\%m\%d).sql
```

## Monitoring

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Health Checks
- Backend: `curl http://yourdomain.com/api/health/`
- Frontend: `curl http://yourdomain.com/`

## Scaling

### Horizontal Scaling (Multiple Instances)

1. Use a load balancer (Nginx, HAProxy, or cloud load balancer)
2. Run multiple backend instances:
```bash
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

3. Use managed database (RDS, Cloud SQL) instead of containerized PostgreSQL

## Troubleshooting

### Container won't start
- Check logs: `docker-compose -f docker-compose.prod.yml logs`
- Verify environment variables: `docker-compose -f docker-compose.prod.yml config`

### Database connection errors
- Verify database is healthy: `docker-compose -f docker-compose.prod.yml ps`
- Check database credentials in `.env`

### Static files not loading
- Run: `docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic`

## Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use strong passwords** - Generate random passwords
3. **Enable HTTPS** - Use Let's Encrypt
4. **Keep dependencies updated** - Regularly update packages
5. **Use firewall** - Only expose necessary ports
6. **Regular backups** - Automate database backups
7. **Monitor logs** - Set up log monitoring
8. **Limit admin access** - Use strong admin passwords

## Maintenance Commands

```bash
# Update application
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Backup database
docker-compose -f docker-compose.prod.yml exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql

# Restore database
docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql
```

## Support

For issues or questions, check:
- Application logs
- Docker container status
- Database connectivity
- Network configuration


