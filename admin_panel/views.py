# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from admin_panel.serializers import *
from rest_framework import generics
from users.permissions import *

User = get_user_model()

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'status': False,
                'message': 'Email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'status': False,
                'message': 'User with this email does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser:
            return Response({
                'status': False,
                'message': 'Access denied. Not an admin user.'
            }, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({
                'status': False,
                'message': 'Incorrect password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': True,
            'message': 'Admin login successful.',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'mobile_number': user.mobile_number
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)
    

class BaseFareListView(generics.ListAPIView):
    serializer_class = BaseFareSerializer
    permission_classes = [IsAdmin]
    queryset = BaseFare.objects.all()

class BaseFareCreateView(generics.CreateAPIView):
    serializer_class = BaseFareSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        fare_type = request.data.get('fare_type')

        if BaseFare.objects.filter(fare_type=fare_type).exists():
            return Response({
                'status': False,
                'message': f"Base fare for '{fare_type}' already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class BaseFareUpdateView(generics.UpdateAPIView):
    serializer_class = BaseFareSerializer
    permission_classes = [IsAdmin]
    queryset = BaseFare.objects.all()
    lookup_field = 'fare_type'

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except BaseFare.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Base fare not found for update.'
            }, status=status.HTTP_404_NOT_FOUND)