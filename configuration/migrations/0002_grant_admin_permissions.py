from django.db import migrations

def grant_admin_permissions_and_seed_params(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    SystemParameter = apps.get_model('configuration', 'SystemParameter')

    # Get or create the Admin role using the PK from data.json to avoid fixture clashes
    admin_role, _ = Role.objects.get_or_create(
        id='02915c14-1092-4733-ae0a-f3067a27b67e',
        defaults={'role_name': 'Admin'}
    )

    # Get the content type for SystemParameter
    try:
        ct_params = ContentType.objects.get(app_label='configuration', model='systemparameter')
    except ContentType.DoesNotExist:
        # If it doesn't exist yet, we might be in a state where it's not created
        # but in migrations it should be there after 0001_initial
        return

    # Get all permissions for this content type
    permissions = Permission.objects.filter(content_type=ct_params)

    # Add permissions to the Admin role
    for perm in permissions:
        admin_role.permissions.add(perm)

    # Seed initial parameters if they don't exist
    params = [
        {
            'name': 'Default Currency',
            'key': 'default_currency',
            'value': 'AED',
            'description': 'The primary currency for all transactions and reporting.',
            'data_type': 'text',
            'category': 'financial',
            'is_public': True
        },
        {
            'name': 'Tax Rate (%)',
            'key': 'tax_rate',
            'value': '5',
            'description': 'Standard VAT or sales tax percentage applied to sales.',
            'data_type': 'number',
            'category': 'financial',
            'is_public': True
        },
        {
            'name': 'Facility Name',
            'key': 'facility_name',
            'value': 'SeaFood Trading Co.',
            'description': 'The name of the facility displayed on reports and invoices.',
            'data_type': 'text',
            'category': 'general',
            'is_public': True
        },
        {
            'name': 'Low Stock Threshold',
            'key': 'low_stock_threshold',
            'value': '10',
            'description': 'Quantity threshold to flag items as low stock.',
            'data_type': 'number',
            'category': 'logistics',
            'is_public': True
        },
        {
            'name': 'Enable Email Notifications',
            'key': 'enable_email_notifications',
            'value': 'True',
            'description': 'Globally enable or disable email notifications.',
            'data_type': 'boolean',
            'category': 'notifications',
            'is_public': False
        },
    ]

    for p_data in params:
        SystemParameter.objects.get_or_create(key=p_data['key'], defaults=p_data)

def remove_admin_permissions(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('configuration', '0001_initial'),
        ('users', '0004_alter_role_created_at_alter_role_updated_at'),
    ]

    operations = [
        migrations.RunPython(grant_admin_permissions_and_seed_params, remove_admin_permissions),
    ]
