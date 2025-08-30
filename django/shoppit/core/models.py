from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Add any additional fields you want for your custom user model
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username