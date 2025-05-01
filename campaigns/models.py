from django.db import models
from users.models import User


class campaign(models.Model):
    worldName = models.CharField(max_length=255)
    description = models.TextField()
    master = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='campaign_master')
    players = models.ManyToManyField(User, related_name='campaign_players')
    isPublic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
