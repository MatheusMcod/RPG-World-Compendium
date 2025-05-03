from rest_framework import serializers
from cloudinary.forms import CloudinaryFileField
from .models import Maps


class UploadedMapsSerializer(serializers.ModelSerializer):
    map = CloudinaryFileField('image')

    class Meta:
        model = Maps
        fields = ['id', 'map', 'uploaded_at']
