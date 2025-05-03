from django.db import models
from cloudinary.models import CloudinaryField


class Maps(models.Model):
    map = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)
