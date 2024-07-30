from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManger


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_organizer = models.BooleanField(default=False)
    organizer_request = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManger()

    def __str__(self):
        return self.email
