from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        if user is None or not user.is_active:
            return Response({"error": "Invalid credentials"}, status=401)
        login(request, user)
        return Response({"message": "Logged in"})

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        logout(self.request)