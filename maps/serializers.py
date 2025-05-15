from rest_framework import serializers
from cloudinary.forms import CloudinaryFileField
from .models import Maps
from campaigns.serializers import CampaignSerializer


class UploadedMapsSerializer(serializers.ModelSerializer):
    map = CloudinaryFileField('image')
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = Maps
        fields = ['id', 'map', 'campaign', 'uploaded_at']
