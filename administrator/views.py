from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Staff
from .serializers import LoginSerializer, StaffSerializer, RoleSerializer, UserSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                try:
                    staff = Staff.objects.get(user=user)
                    role = staff.Role.RoleName
                except Staff.DoesNotExist:
                    role = 'Unknown'

                return Response({
                    'token': token.key,
                    'username': user.username,
                    'role': role,
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Example of Role-protected API
from rest_framework.authentication import TokenAuthentication

class AdminOnlyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.Role.RoleName != 'Admin':
                return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'message': 'Welcome Admin'})
        except Staff.DoesNotExist:
            return Response({'error': 'Staff profile not found'}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.
