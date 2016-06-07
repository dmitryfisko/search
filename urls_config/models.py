from django.db import models

# Create your models here.
class Url(models.Model):
    path = models.CharField(max_length=255)
    title = models.TextField()
