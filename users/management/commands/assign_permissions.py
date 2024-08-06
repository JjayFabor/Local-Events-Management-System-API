from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Assign permissions to Residents and Government Authority groups"

    def handle(self, *args, **kwargs):
        # Assign permissions to Residents group
        residents_group, created = Group.objects.get_or_create(name="Residents")
        resident_perms = ["view_event", "change_user", "delete_user"]
        for perm in resident_perms:
            try:
                permission = Permission.objects.get(codename=perm)
                residents_group.permissions.add(permission)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added {perm} permission to Residents group"
                    )
                )
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Permession {perm} does not exist"))

        # Assign permissions to Governement Authority group
        governement_group, created = Group.objects.get_or_create(
            name="Governement Authority"
        )
        gov_perms = [
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
        ]
        for perm in gov_perms:
            try:
                permission = Permission.objects.get(codename=perm)
                governement_group.permissions.add(permission)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added {perm} permission to Governement Authority group"
                    )
                )
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Permession {perm} does not exist"))

        self.stdout.write(
            self.style.SUCCESS("Permissions have been successfully assigned")
        )
