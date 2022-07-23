from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video")
    size = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=3)
    duration = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=4)

    def __str__(self):
        return self.caption
