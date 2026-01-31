#!/bin/bash

# Ankur Application Deployment Script
# Usage: ./deploy.sh [production|development]

set -e

ENV=${1:-production}
COMPOSE_FILE="docker-compose.yml"

if [ "$ENV" = "production" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    echo "🚀 Deploying to PRODUCTION..."
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        echo "❌ Error: .env file not found!"
        echo "📝 Creating .env from .env.example..."
        cp .env.example .env
        echo "⚠️  Please edit .env file with your production values before deploying!"
        echo "   Especially: SECRET_KEY, POSTGRES_PASSWORD, ALLOWED_HOSTS"
        exit 1
    fi
    
    echo "✅ Using production configuration"
else
    echo "🔧 Deploying to DEVELOPMENT..."
    COMPOSE_FILE="docker-compose.yml"
fi

echo "📦 Building and starting containers..."
docker-compose -f $COMPOSE_FILE up -d --build

echo "⏳ Waiting for services to be ready..."
sleep 5

echo "🔄 Running database migrations..."
docker-compose -f $COMPOSE_FILE exec -T backend python manage.py migrate || echo "⚠️  Migration failed, but continuing..."

echo "📊 Collecting static files..."
docker-compose -f $COMPOSE_FILE exec -T backend python manage.py collectstatic --noinput || echo "⚠️  Static files collection failed, but continuing..."

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Service Status:"
docker-compose -f $COMPOSE_FILE ps

echo ""
if [ "$ENV" = "production" ]; then
    echo "🌐 Your application should be available at:"
    echo "   - Frontend: http://localhost (or your configured domain)"
    echo "   - Admin: http://localhost/admin/"
    echo "   - API: http://localhost/api/"
else
    echo "🌐 Your application should be available at:"
    echo "   - Frontend: http://localhost:4200"
    echo "   - Backend: http://localhost:8000"
    echo "   - Admin: http://localhost:8000/admin/"
fi

echo ""
echo "💡 To create a superuser, run:"
echo "   docker-compose -f $COMPOSE_FILE exec backend python manage.py createsuperuser"
echo ""
echo "📝 To view logs, run:"
echo "   docker-compose -f $COMPOSE_FILE logs -f"



