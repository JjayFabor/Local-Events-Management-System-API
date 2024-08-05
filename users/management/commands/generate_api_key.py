from django.core.management.base import BaseCommand
from users.models import ApiKey


class Command(BaseCommand):
    help = "Generates a new API key"

    def handle(self, *args, **kwargs):
        api_key = ApiKey.create_key()
        self.stdout.write(self.style.SUCCESS(f"Generated new API key: {api_key.key}"))
