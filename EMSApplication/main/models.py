
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LogPath(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    enabled = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)