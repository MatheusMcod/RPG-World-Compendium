from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from .models import Campaigns, Invite, JoinRequest


class CampaignSerializer(serializers.ModelSerializer):
    master_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='master', write_only=True)
    players = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Campaigns
        fields = [
            'id',
            'worldName',
            'description',
            'master_id',
            'players',
            'isPublic',
            'created_at',
            'updated_at'
        ]


class InviteSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(read_only=True)
    invited_user = UserSerializer(read_only=True)
    invited_by = UserSerializer(read_only=True)
  
    class Meta:
        model = Invite
        fields = ['id', 'campaign', 'invited_user',
                  'invited_by', 'accepted', 'status', 'created_at']
        read_only_fields = ['invited_by', 'accepted', 'status', 'created_at']


class InviteConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['status']


class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = ['id', 'campaign', 'user', 'accepted', 'status', 'created_at']
        read_only_fields = ['user', 'accepted', 'status', 'created_at']


class JoinConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = ['status']