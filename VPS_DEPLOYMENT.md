# VPS Deployment Guide

Complete guide for deploying Ankur application on a VPS (Virtual Private Server).

## Prerequisites

- VPS with Ubuntu 22.04 (or similar)
- SSH access to your VPS
- Domain name (optional, but recommended)

## Step 1: Choose VPS Provider

### Recommended Providers:
- **DigitalOcean**: $6/month (1GB RAM, 1 vCPU)
- **Linode**: $5/month
- **Vultr**: $6/month
- **Hetzner**: €4.51/month (Europe)

### Create VPS:
1. Sign up with provider
2. Create new Droplet/Instance
3. Choose Ubuntu 22.04
4. Select smallest plan ($5-6/month)
5. Add SSH key or set root password
6. Create instance

## Step 2: Initial Server Setup

### Connect to Server:
```bash
ssh root@your-server-ip
```

### Update System:
```bash
apt update && apt upgrade -y
```

### Create Non-Root User:
```bash
adduser ankur
usermod -aG sudo ankur
su - ankur
```

### Install Docker:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in for group changes
exit
# SSH back in
```

### Install Git:
```bash
sudo apt install git -y
```

## Step 3: Deploy Application

### Clone Repository:
```bash
cd ~
git clone <your-repo-url> ankur
cd ankur
```

### Create Environment File:
```bash
cp .env.example .env
nano .env
```

Edit with your values:
```env
POSTGRES_DB=ankur_db
POSTGRES_USER=ankur_user
POSTGRES_PASSWORD=YourStrongPassword123!

SECRET_KEY=generate-with-python-secrets-token_urlsafe-50
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

FRONTEND_PORT=80
REACT_APP_API_URL=http://yourdomain.com/api
CORS_ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com
```

### Generate Secret Key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Deploy:
```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d --build
```

### Create Superuser:
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

## Step 4: Configure Firewall

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## Step 5: Set Up Domain (Optional)

### Point Domain to Server:
1. Go to your domain registrar
2. Add A record: `@` → your-server-ip
3. Add A record: `www` → your-server-ip

### Wait for DNS Propagation:
```bash
# Check DNS
dig yourdomain.com
```

## Step 6: Set Up SSL with Let's Encrypt

### Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Get Certificate:
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### Auto-Renewal:
Certbot sets up auto-renewal automatically. Test with:
```bash
sudo certbot renew --dry-run
```

## Step 7: Configure Nginx (Optional - for better performance)

### Install Nginx:
```bash
sudo apt install nginx -y
```

### Create Nginx Config:
```bash
sudo nano /etc/nginx/sites-available/ankur
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable Site:
```bash
sudo ln -s /etc/nginx/sites-available/ankur /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: Set Up Auto-Start

### Create Systemd Service (Optional):
```bash
sudo nano /etc/systemd/system/ankur.service
```

Add:
```ini
[Unit]
Description=Ankur Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ankur/ankur
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml --env-file .env up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
User=ankur
Group=ankur

[Install]
WantedBy=multi-user.target
```

### Enable Service:
```bash
sudo systemctl enable ankur.service
sudo systemctl start ankur.service
```

## Step 9: Set Up Backups

### Create Backup Script:
```bash
mkdir -p ~/backups
nano ~/backup.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cd /home/ankur/ankur
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ankur_user ankur_db > ~/backups/ankur_$DATE.sql
# Keep only last 7 days
find ~/backups -name "ankur_*.sql" -mtime +7 -delete
```

### Make Executable:
```bash
chmod +x ~/backup.sh
```

### Add to Crontab:
```bash
crontab -e
```

Add:
```
0 2 * * * /home/ankur/backup.sh
```

## Step 10: Monitoring

### View Logs:
```bash
cd ~/ankur
docker-compose -f docker-compose.prod.yml logs -f
```

### Check Status:
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Monitor Resources:
```bash
# CPU and Memory
htop

# Disk space
df -h

# Docker stats
docker stats
```

## Maintenance Commands

### Update Application:
```bash
cd ~/ankur
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

### Run Migrations:
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### Restart Services:
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Stop Services:
```bash
docker-compose -f docker-compose.prod.yml down
```

## Troubleshooting

### Container Won't Start:
```bash
docker-compose -f docker-compose.prod.yml logs
```

### Database Connection Issues:
```bash
docker-compose -f docker-compose.prod.yml exec db psql -U ankur_user -d ankur_db
```

### Port Already in Use:
```bash
sudo netstat -tulpn | grep :80
sudo kill <PID>
```

### Out of Disk Space:
```bash
docker system prune -a
```

## Security Checklist

- [ ] Changed default SSH port (optional)
- [ ] Set up SSH key authentication
- [ ] Configured firewall
- [ ] Set strong passwords
- [ ] Installed SSL certificate
- [ ] Set up automated backups
- [ ] Enabled fail2ban (optional)
- [ ] Regular system updates

## Cost Estimate

- VPS: $5-6/month
- Domain: $10-15/year (optional)
- **Total: ~$6-7/month**

## Next Steps

1. Set up monitoring (UptimeRobot - free)
2. Configure email notifications
3. Set up CI/CD (GitHub Actions)
4. Add CDN for static assets (Cloudflare - free)



