from django.db.models.signals import post_save, post_migrate
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from events.models import EventModel, Category
from .models import CustomUser
from django.contrib.auth import get_user_model


@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        resident_group, created = Group.objects.get_or_create(name="Residents")
        instance.groups.add(resident_group)
        # print(f"Added {instance.email} to Residents group.")
