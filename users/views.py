from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import User
from .serializers import CustomTokenObtainPairSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # type: ignore


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if not request.data.get('refresh'):
            refresh_token = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE'])
            if refresh_token:
                request.data['refresh'] = refresh_token

        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout successful"},
                            status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        return response


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "username": user.name,
        }
        return Response(data)
