from django.db import models
from django.contrib.auth.models import AbstractUser



class Role(models.TextChoices):
     READER =  'Reader'
     ADMIN =  'Admin'
     CREATOR =  'Creator'


class User (AbstractUser):
    role = models.CharField( max_length=20,  choices=Role.choices, default=Role.READER)

    def __str__(self):
        return f"{self.username}"








