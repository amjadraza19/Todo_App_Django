from django.contrib.auth.models import AbstractUser
from django.db import models


class TodoUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return self.username
