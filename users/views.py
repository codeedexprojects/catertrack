# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import *
from .models import User
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class createuserview(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'status': True,
                'message': 'User registered successfully',
                'user': UserDetailSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status':False,
            'message': 'Validation failed',
            'errors': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "status": True,
            "user": UserDetailSerializer(request.user).data
        })

class StaffDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.staff_details
        except StaffDetails.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'Staff details not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'status': False, 'message': 'Staff details not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'status': False, 'message': 'Staff details not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class StaffDetailsCreateView(generics.CreateAPIView):
    serializer_class = StaffDetailsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'staff_details'):
            return Response({'status': False, 'message': 'Staff details already exist.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': True, 'message': 'Staff details created.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'User profile updated successfully.',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)