from django.db.models.signals import post_save, post_migrate
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from events.models import EventModel, Category
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_government_authority:
            government_group, created = Group.objects.get_or_create(
                name="Government Authority"
            )
            instance.groups.add(government_group)
        else:
            resident_group, created = Group.objects.get_or_create(name="Residents")
            instance.groups.add(resident_group)

        # Ensure no other permissions are assigned
        if not instance.is_government_authority:
            instance.user_permissions.clear()


@receiver(post_migrate)
def setup_permissions(sender, **kwargs):
    if sender.name == "users":  # Ensure this runs only for the 'users' app
        # Create or get the 'Residents' group
        resident_group, created = Group.objects.get_or_create(name="Residents")

        # Create or get the 'Government Authority' group
        government_group, created = Group.objects.get_or_create(
            name="Government Authority"
        )

        # Define the content types
        user_content_type = ContentType.objects.get_for_model(CustomUser)
        event_content_type = ContentType.objects.get_for_model(EventModel)
        category_content_type = ContentType.objects.get_for_model(Category)

        # Define the permission codenames
        permission_codenames = {
            "Residents": ["view_event", "change_user", "delete_user"],
            "Government Authority": [
                "add_event",
                "change_event",
                "delete_event",
                "view_event",
                "add_category",
                "change_category",
                "delete_category",
                "view_user",
                "add_user",
                "change_user",
                "delete_user",
            ],
        }

        # Clear existing permissions
        resident_group.permissions.clear()
        government_group.permissions.clear()

        # Helper function to add permissions
        def add_permissions(group, codenames, content_type):
            for codename in codenames:
                try:
                    permission = Permission.objects.get(
                        codename=codename, content_type=content_type
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(
                        f"Permission {codename} does not exist for {group.name} group"
                    )

        # Add permissions to the 'Residents' group
        add_permissions(resident_group, ["view_event"], event_content_type)
        add_permissions(
            resident_group, ["change_user", "delete_user"], user_content_type
        )

        # Add permissions to the 'Government Authority' group
        add_permissions(
            government_group,
            ["add_event", "change_event", "delete_event", "view_event"],
            event_content_type,
        )
        add_permissions(
            government_group,
            ["add_category", "change_category", "delete_category"],
            category_content_type,
        )
        add_permissions(
            government_group,
            ["view_user", "add_user", "change_user", "delete_user"],
            user_content_type,
        )

        print("Permissions set up for 'Residents' and 'Government Authority' groups.")
