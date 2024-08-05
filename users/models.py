from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManger


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    events_joined = models.ManyToManyField(
        "events.EventModel", related_name="participants", blank=True
    )
    is_government_authority = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManger()

    def __str__(self):
        return self.email

    @property
    def is_resident(self):
        return not self.is_government_authority and not self.is_superuser
