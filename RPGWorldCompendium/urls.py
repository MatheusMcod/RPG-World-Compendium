from django.contrib import admin
from django.urls import path, include
from users import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include(urls.authUrlpatterns)),
]
