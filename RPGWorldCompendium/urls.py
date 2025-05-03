from django.contrib import admin
from django.urls import path, include
from users import urls as userUrls
from campaigns import urls as campaignUrls
from maps import urls as mapsUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include(userUrls.authUrlpatterns)),
    path('api/v1/campaign/', include(campaignUrls.urlpatterns)),
    path('api/v1/maps/', include(mapsUrls.urlpatterns)),
]
