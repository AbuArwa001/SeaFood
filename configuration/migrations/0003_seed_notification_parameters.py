from django.db import migrations

def seed_notification_parameters(apps, schema_editor):
    SystemParameter = apps.get_model('configuration', 'SystemParameter')
    
    parameters = [
        {
            'name': 'Overdue Payment Alert Threshold',
            'key': 'notify_overdue_payment_days',
            'value': '1',
            'description': 'Number of days past the expected payment date to trigger a notification.',
            'data_type': 'number',
            'category': 'notifications',
            'is_public': True
        },
        {
            'name': 'Shipment Arriving Soon Threshold',
            'key': 'notify_shipment_arriving_soon_days',
            'value': '2',
            'description': 'Number of days before estimated arrival to trigger an "arriving soon" notification.',
            'data_type': 'number',
            'category': 'notifications',
            'is_public': True
        },
        {
            'name': 'Notification Admin Email',
            'key': 'notify_admin_email',
            'value': 'khalfanathman12@gmail.com',
            'description': 'Email address to receive critical notification copies.',
            'data_type': 'text',
            'category': 'notifications',
            'is_public': True
        },
        {
            'name': 'Enable Automated Email Notifications',
            'key': 'enable_automated_emails',
            'value': 'true',
            'description': 'Globally enable or disable automated email triggers for overdue events.',
            'data_type': 'boolean',
            'category': 'notifications',
            'is_public': True
        },
        {
            'name': 'Notification Recipient Roles',
            'key': 'notify_roles',
            'value': '["Admin", "Finance Agent", "Sales Agent"]',
            'description': 'JSON list of user roles that should receive system-wide notifications.',
            'data_type': 'json',
            'category': 'notifications',
            'is_public': True
        }
    ]

    for param in parameters:
        SystemParameter.objects.update_or_create(
            key=param['key'],
            defaults=param
        )

def remove_notification_parameters(apps, schema_editor):
    SystemParameter = apps.get_model('configuration', 'SystemParameter')
    keys = [
        'notify_overdue_payment_days',
        'notify_shipment_arriving_soon_days',
        'notify_admin_email',
        'enable_automated_emails',
        'notify_roles'
    ]
    SystemParameter.objects.filter(key__in=keys).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_grant_admin_permissions'),
    ]

    operations = [
        migrations.RunPython(seed_notification_parameters, remove_notification_parameters),
    ]
