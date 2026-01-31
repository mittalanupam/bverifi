from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    
    # Authentication endpoints
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/user/', views.CurrentUserView.as_view(), name='current_user'),
    
    # Application statistics
    path('applications/stats/', views.application_stats, name='application_stats'),
    
    # Router URLs
    path('', include(router.urls)),
]
