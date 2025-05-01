from rest_framework import serializers
from users.serializers import UserSerializer
from .models import campaign, Invite
from users.models import User


class CampaignSerializer(serializers.ModelSerializer):
    master_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='master', write_only=True)
    players = UserSerializer(many=True, read_only=True)

    class Meta:
        model = campaign
        fields = [
            'id',
            'worldName',
            'description',
            'master',
            'players',
            'isPublic',
            'created_at',
            'updated_at'
        ]


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['id', 'campaign', 'invited_user',
                  'invited_by', 'accepted', 'created_at']
        read_only_fields = ['invited_by', 'accepted', 'created_at']
