from django.db import models

# Create your models here.
class Profile(models.Model):
    email = models.CharField(max_length=200, unique=True)
    type = models.IntegerField(default=0)