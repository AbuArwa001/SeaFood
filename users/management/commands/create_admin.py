from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import Permission
from seafood.settings import ROLE_CAPABILITIES
from users.models import User, Role
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Create admin user if it does not exist"


    def handle(self, *args, **kwargs):
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD
        location = settings.ADMIN_LOCATION
        # roles = settings.ADMIN_ROLES
        role_capabilities = ROLE_CAPABILITIES
        permissions = Permission.objects.all()

        roles = parse_roles(settings.ADMIN_ROLES)
        print(f"Configuring roles: {roles} ADMIN ROLES: {settings.ADMIN_ROLES}")

        ROLE_PERMISSION_MAP = build_role_permission_map(roles)

        for role_name, perms in ROLE_PERMISSION_MAP.items():
            print(f"Setting up role: {role_name} with {perms.count()} permissions")
            role, _ = Role.objects.get_or_create(role_name=role_name)
            role.permissions.set(perms)
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

def parse_roles(env_value):
    return [r.strip() for r in env_value.split(",") if r.strip()]

def build_role_permission_map(role_names):
    role_map = {}

    for role in role_names:
        config = ROLE_CAPABILITIES.get(role)

        if not config:
            continue  # ignore unknown roles

        if config == "__all__":
            role_map[role] = Permission.objects.all()
        else:
            role_map[role] = get_permissions_for_apps(
                app_labels=config["apps"],
                actions=config["actions"]
            )

    return role_map

def get_permissions_for_apps(app_labels, actions):
    permissions = Permission.objects.none()

    for app_label in app_labels:
        content_types = ContentType.objects.filter(app_label=app_label)

        perms = Permission.objects.filter(
            content_type__in=content_types,
            codename__regex=rf"^({'|'.join(actions)})_"
        )

        permissions |= perms

    return permissions
