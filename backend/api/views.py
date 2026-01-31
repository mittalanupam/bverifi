from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Item, Application
from .serializers import (
    ItemSerializer, ApplicationListSerializer, ApplicationDetailSerializer, UserSerializer
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check endpoint."""
    return Response({'status': 'healthy', 'message': 'Django API is running!'})


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for Item CRUD operations."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# ============ Authentication Views ============

class LoginView(APIView):
    """Login endpoint for agents"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """Logout endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout successful'})
        except Exception:
            return Response({'message': 'Logout successful'})


class CurrentUserView(APIView):
    """Get current authenticated user info"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ============ Application Views ============

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application CRUD operations.
    
    Endpoints:
    - GET /api/applications/ - List all applications for the current user
    - POST /api/applications/ - Create a new application
    - GET /api/applications/{id}/ - Get application details
    - PUT /api/applications/{id}/ - Update application
    - DELETE /api/applications/{id}/ - Delete application
    - POST /api/applications/{id}/submit/ - Submit/finalize application
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return applications for the current authenticated user"""
        return Application.objects.filter(agent=self.request.user).select_related(
            'business_details', 'co_applicant', 'security_details', 'conclusion'
        ).prefetch_related(
            'other_businesses', 'loans', 'bank_accounts',
            'business_details__owners', 'business_details__persons_met'
        )
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new application"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        
        # Return the full application details
        detail_serializer = ApplicationDetailSerializer(
            application, context={'request': request}
        )
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Mark application as submitted/finalized"""
        application = self.get_object()
        
        # Check if conclusion exists (required for submission)
        if not hasattr(application, 'conclusion'):
            return Response(
                {'error': 'Application must have a conclusion before submission'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Application submitted successfully',
            'application_id': application.id,
            'file_no': application.file_no,
            'overall_status': application.conclusion.overall_status
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def application_stats(request):
    """Get application statistics for the current user"""
    applications = Application.objects.filter(agent=request.user)
    
    total = applications.count()
    positive = applications.filter(conclusion__overall_status='Positive').count()
    negative = applications.filter(conclusion__overall_status='Negative').count()
    refer_to_credit = applications.filter(conclusion__overall_status='Refer to credit').count()
    pending = total - positive - negative - refer_to_credit
    
    return Response({
        'total': total,
        'positive': positive,
        'negative': negative,
        'refer_to_credit': refer_to_credit,
        'pending': pending
    })
