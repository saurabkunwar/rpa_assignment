from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video")

    def __str__(self):
        return self.caption
