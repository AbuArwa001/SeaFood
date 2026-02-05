from django.core.management.base import BaseCommand
from users.models import User, Role
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with test users for each role'

    def handle(self, *args, **options):
        self.stdout.write('Seeding users for RBAC testing...')

        roles_users = {
            'Admin': 'admin@seafood.com',
            'Mozambique Agent': 'mozambique@seafood.com',
            'Logistics Agent': 'logistics@seafood.com',
            'Sales Agent': 'sales@seafood.com',
            'Finance Agent': 'finance@seafood.com',
            'Viewer': 'viewer@seafood.com'
        }

        default_password = 'password123'

        for role_name, email in roles_users.items():
            role, _ = Role.objects.get_or_create(role_name=role_name)
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': f'Test {role_name}',
                    'location': 'Headquarters',
                    'role': role
                }
            )
            
            if created:
                user.set_password(default_password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {email} ({role_name})'))
            else:
                # Update password just in case
                user.set_password(default_password)
                user.save()
                self.stdout.write(f'Updated user: {email} ({role_name})')

        self.stdout.write(self.style.SUCCESS(f'All users seeded with password: "{default_password}"'))
