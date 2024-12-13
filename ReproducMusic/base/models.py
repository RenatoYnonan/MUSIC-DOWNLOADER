from django.db import models

# Create your models here.

class Music(models.Model):
    url = models.URLField(max_length=200, unique=True)