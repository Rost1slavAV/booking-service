from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length = 100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default = 0)

    def __str__(self):
        return self.username