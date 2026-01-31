# Ankur - Full Stack Application

A modern full-stack application with **Django** backend, **React** frontend, and **PostgreSQL** database, all containerized with **Docker**.

## 🚀 Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: React 18 with Hooks
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
ankur/
├── backend/                 # Django backend
│   ├── api/                 # REST API app
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # API views
│   │   └── urls.py          # API routes
│   ├── backend/             # Django project settings
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js           # Main component
│   │   ├── App.css          # Styles
│   │   └── index.js         # Entry point
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml       # Docker orchestration
├── .env                     # Environment variables
└── README.md
```

## 🛠️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

## 🏃 Quick Start

### 1. Clone and navigate to the project

```bash
cd /home/ankita/workspace/ankur
```

### 2. Start all services

```bash
docker-compose up --build
```

This command will:
- Build the Docker images for backend and frontend
- Start PostgreSQL database
- Run Django migrations automatically
- Start the Django development server
- Start the React development server

### 3. Access the application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API Health Check**: http://localhost:8000/api/health/

## 📋 Available Commands

### Docker Commands

```bash
# Start all services
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# Build and start
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Django Management Commands

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser for admin access
docker-compose exec backend python manage.py createsuperuser

# Make migrations
docker-compose exec backend python manage.py makemigrations

# Django shell
docker-compose exec backend python manage.py shell

# Collect static files
docker-compose exec backend python manage.py collectstatic
```

### Database Commands

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U ankur_user -d ankur_db

# Database backup
docker-compose exec db pg_dump -U ankur_user ankur_db > backup.sql

# Database restore
docker-compose exec -T db psql -U ankur_user -d ankur_db < backup.sql
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check |
| GET | `/api/items/` | List all items |
| POST | `/api/items/` | Create new item |
| GET | `/api/items/{id}/` | Get item details |
| PUT | `/api/items/{id}/` | Update item |
| PATCH | `/api/items/{id}/` | Partial update |
| DELETE | `/api/items/{id}/` | Delete item |

## ⚙️ Environment Variables

Edit the `.env` file to customize:

```env
# Database
POSTGRES_DB=ankur_db
POSTGRES_USER=ankur_user
POSTGRES_PASSWORD=ankur_password

# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

## 🔧 Development

### Backend Development

The backend code is mounted as a volume, so changes will be reflected immediately (Django's auto-reload).

### Frontend Development

The frontend also uses volume mounting with hot-reload enabled. Changes to React code will automatically update in the browser.

### Adding New Dependencies

**Backend (Python)**:
```bash
# Add to requirements.txt, then rebuild
docker-compose build backend
docker-compose up -d backend
```

**Frontend (Node.js)**:
```bash
# Add to package.json, then rebuild
docker-compose build frontend
docker-compose up -d frontend
```

## 🚀 Production Deployment

For production, consider:

1. Use `gunicorn` instead of Django's development server
2. Add nginx as a reverse proxy
3. Use proper secret keys (change `SECRET_KEY`)
4. Set `DEBUG=False`
5. Configure proper CORS settings
6. Use SSL/TLS certificates
7. Set up proper logging and monitoring

## 🐛 Troubleshooting

### Database connection issues
```bash
# Check if database is healthy
docker-compose ps

# Restart the database
docker-compose restart db
```

### Frontend not connecting to backend
- Ensure CORS is properly configured
- Check that `REACT_APP_API_URL` matches your backend URL

### Hot reload not working
- Ensure `CHOKIDAR_USEPOLLING=true` is set for the frontend
- Try restarting the containers

## 📝 License

MIT License - feel free to use this project as a template!

# bverifi
