# How to Access Application Forms

## Forms Location

The application forms are static HTML files located in:
- `/frontend/public/application-form/form.html` - Main application form
- `/frontend/public/application-form/list.html` - List of applications

## Access URLs

Once the frontend is running on port 4200, you can access the forms at:

1. **Application Form**: http://localhost:4200/application-form/form.html
2. **Applications List**: http://localhost:4200/application-form/list.html

## Current Status

✅ Frontend is running on port 4200
✅ Backend API is running on port 8000
✅ Forms are being served (HTTP 200 response)
✅ API endpoints are working

## Troubleshooting

If forms are not displaying:

1. **Check Browser Console**: Open browser developer tools (F12) and check for JavaScript errors
2. **Verify URLs**: Make sure you're accessing the correct URLs:
   - http://localhost:4200/application-form/form.html
   - http://localhost:4200/application-form/list.html
3. **Check API Connection**: The forms connect to http://localhost:8000/api
4. **Create a Test User**: You need to create a user account to login:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## Quick Test

1. Open http://localhost:4200/application-form/form.html in your browser
2. You should see a login form
3. Create a superuser if you haven't already
4. Login with your credentials
5. The application form should appear



