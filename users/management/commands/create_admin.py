from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User, Role

class Command(BaseCommand):
    help = "Create admin user if it does not exist"

    def handle(self, *args, **kwargs):
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD
        location = settings.ADMIN_LOCATION

        if not email or not password:
            self.stdout.write("Admin env vars not set")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write("Admin user already exists")
            return

        admin_role = Role.objects.get(role_name="Admin")

        User.objects.create_superuser(
            email=email,
            password=password,
            full_name="Managing Director",
            location=location,
            role=admin_role
        )

        self.stdout.write(self.style.SUCCESS("Admin user created"))
