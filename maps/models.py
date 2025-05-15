from cloudinary.models import CloudinaryField
from django.db import models


class Maps(models.Model):
    campaign = models.ForeignKey('campaigns.Campaigns', on_delete=models.CASCADE,
                                 related_name='maps')
    map = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)
