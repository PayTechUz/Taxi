from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OPERATOR = "OPERATOR", "Operator"
        DRIVER = "DRIVER", "Driver"
        CLIENT = "CLIENT", "Client"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CLIENT)

    def __str__(self):
        return self.username
