from django.urls import path

from .views import (CustomCookieTokenRefreshView, CustomTokenObtainPairView,
                    GetUserView, RegisterView)

authUrlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(),
         name='token_pair'),
    path('auth/refresh/', CustomCookieTokenRefreshView.as_view(),
         name='token_refresh'),
    path('', GetUserView.as_view(), name='get_user'),
]
