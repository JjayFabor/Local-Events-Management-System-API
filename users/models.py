from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManger
import secrets


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

    class Meta:
        permissions = [
            ("view_user", "Can view user"),
            ("change_user", "Can change user"),
            ("delete_user", "Can delete user"),
            ("add_user", "Can add user"),
        ]

    def __str__(self):
        return self.email

    @property
    def is_resident(self):
        return not self.is_government_authority and not self.is_superuser


class ApiKey(models.Model):
    key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    def generate_key():
        return secrets.token_urlsafe(32)

    @classmethod
    def create_key(cls):
        key = cls.generate_key()
        return cls.objects.create(key=key)
