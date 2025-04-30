from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CustomTokenRefreshView, CustomTokenObtainPairView,
                    GetUserView, RegisterView, LogoutView)

authUrlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(),
         name='token_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('', GetUserView.as_view(), name='get_user'),
]
