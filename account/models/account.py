from django.contrib.auth.models import AbstractUser
from django.db import models

from account.models.base import BaseModel


class Account(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
