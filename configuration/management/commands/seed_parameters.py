from django.core.management.base import BaseCommand
from configuration.models import SystemParameter, ParameterType, ParameterCategory

class Command(BaseCommand):
    help = 'Seeds initial system parameters'

    def handle(self, *args, **kwargs):
        parameters = [
            {
                "name": "Facility Name",
                "key": "facility_name",
                "value": "SeaFood Trading Co.",
                "description": "The name of the facility displayed on reports and invoices.",
                "data_type": ParameterType.TEXT,
                "category": ParameterCategory.GENERAL,
                "is_public": True,
            },
            {
                "name": "Default Currency",
                "key": "default_currency",
                "value": "AED",
                "description": "Default currency used for system-wide calculations.",
                "data_type": ParameterType.TEXT,
                "category": ParameterCategory.FINANCIAL,
                "is_public": True,
            },
            {
                "name": "Tax Rate (%)",
                "key": "tax_rate",
                "value": "5",
                "description": "Default VAT/Tax rate applied to sales.",
                "data_type": ParameterType.NUMBER,
                "category": ParameterCategory.FINANCIAL,
                "is_public": True,
            },
            {
                "name": "Enable Email Notifications",
                "key": "enable_email_notifications",
                "value": "True",
                "description": "Globally enable or disable email notifications.",
                "data_type": ParameterType.BOOLEAN,
                "category": ParameterCategory.NOTIFICATIONS,
                "is_public": False,
            },
            {
                "name": "Low Stock Threshold",
                "key": "low_stock_threshold",
                "value": "10",
                "description": "Quantity threshold to flag items as low stock.",
                "data_type": ParameterType.NUMBER,
                "category": ParameterCategory.LOGISTICS,
                "is_public": True,
            },
        ]

        for p_data in parameters:
            parameter, created = SystemParameter.objects.get_or_create(
                key=p_data["key"],
                defaults=p_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created parameter: {parameter.key}'))
            else:
                self.stdout.write(self.style.WARNING(f'Parameter already exists: {parameter.key}'))
