from django.contrib.auth.models import AbstractUser

from account.models.base import BaseModel


class Account(BaseModel, AbstractUser):
    pass
