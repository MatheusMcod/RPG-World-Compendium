from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import RegisterView, CustomTokenObtainPairView


authUrlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
