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

        # Permission Map
        role_permissions = {
            'Admin': '__all__',
            'Mozambique Agent': [
                'view_supplierpurchase', 'add_supplierpurchase', 'change_supplierpurchase',
                'view_shipment', 'add_shipment', 'change_shipment',
                'view_logisticsreceipt', 'add_logisticsreceipt',
            ],
            'Logistics Agent': [
                 'view_shipment', 'change_shipment',
                 'view_logisticsreceipt', 'add_logisticsreceipt', 'change_logisticsreceipt',
                 'view_costledger', 'add_costledger',
            ],
            'Sales Agent': [
                'view_sale', 'add_sale', 'change_sale',
                'view_shipment', 'view_product',
            ],
            'Finance Agent': [
                'view_payment', 'add_payment', 'change_payment',
                'view_sale', 'view_costledger', 'view_exchangerate', 'view_currency'
            ],
            'Viewer': [
                'view_shipment', 'view_product', 'view_sale'
            ]
        }

        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        for role_name, email in roles_users.items():
            role, _ = Role.objects.get_or_create(role_name=role_name)
            
            # Assign Permissions
            codenames = role_permissions.get(role_name, [])
            if codenames == '__all__':
                role.permissions.set(Permission.objects.all())
            else:
                perms = []
                for codename in codenames:
                    try:
                        p = Permission.objects.get(codename=codename)
                        perms.append(p)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permission '{codename}' not found"))
                role.permissions.set(perms)
            role.save()

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
                user.set_password(default_password)
                user.save()
                self.stdout.write(f'Updated user: {email} ({role_name})')

        self.stdout.write(self.style.SUCCESS(f'All users seeded with password: "{default_password}" and permissions assigned.'))
