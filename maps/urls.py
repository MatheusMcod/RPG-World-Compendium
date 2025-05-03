from django.urls import path
from .views import MapsUploadView

urlpatterns = [
    path('upload/', MapsUploadView.as_view(), name='maps-upload'),
]