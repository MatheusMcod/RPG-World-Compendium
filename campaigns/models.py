from django.db import models

from users.models import User


class Campaigns(models.Model):
    worldName = models.CharField(max_length=255)
    description = models.TextField()
    master = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='campaign_master')
    players = models.ManyToManyField(User, related_name='campaign_players')
    isPublic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Invite(models.Model):
    campaign = models.ForeignKey('Campaigns', on_delete=models.CASCADE,
                                 related_name='invites')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='invites_received')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='invites_sent')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'invited_user')

    def __str__(self):
        return f"Convite para {self.invited_user.username} na campanha {self.campaign.worldName}"
