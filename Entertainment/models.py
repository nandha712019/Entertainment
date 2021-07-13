import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Media(models.Model):
    """Database table for Media details!!!"""
    Media_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Media_link = models.FileField(upload_to="uploads/", unique=True)
    Media_type = models.CharField('Media_type', max_length=20, default='Audio',
                                  choices=[('Audio', 'Audio'), ('Video', 'Video')])
    Title = models.TextField(max_length=50, default="")
    Description = models.TextField(max_length=300, default="")
    Thumbnail = models.ImageField(upload_to="uploads/")
    created_on = models.DateTimeField(default=datetime.now)


class Favourite(models.Model):
    """Database table for Favourite"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    Media_id = models.ForeignKey(Media, on_delete=models.CASCADE, )

    class Meta:
        unique_together = ["user", "Media_id"]
