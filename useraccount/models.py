from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Added 2 fields to default user class: 
    postcode and pending status"""
    postcode = models.CharField(max_length=5)
    verified_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username
