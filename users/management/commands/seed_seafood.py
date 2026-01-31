import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from currencies.models import Currency
from unitofmeasures.models import UnitOfMeasure
from productcategories.models import ProductCategory
from products.models import Product
from exchangerates.models import ExchangeRate
from shipments.models import Shipment, ShipmentItem

class Command(BaseCommand):
    help = 'Seeds the database with initial SeaFood data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Currencies
        usd, _ = Currency.objects.get_or_create(code='USD', defaults={'name': 'US Dollar', 'symbol': '$'})
        kes, _ = Currency.objects.get_or_create(code='KES', defaults={'name': 'Kenyan Shilling', 'symbol': 'KSh'})
        self.stdout.write(f'Created currencies: {usd}, {kes}')

        # 2. Exchange Rates
        ExchangeRate.objects.get_or_create(
            from_currency=kes,
            to_currency=usd,
            rate_date=timezone.now().date(),
            defaults={'rate': Decimal('0.0078')} # 1 KES = 0.0078 USD
        )
        ExchangeRate.objects.get_or_create(
            from_currency=usd,
            to_currency=kes,
            rate_date=timezone.now().date(),
            defaults={'rate': Decimal('128.50')} # 1 USD = 128.50 KES
        )

        # 3. Units of Measure
        kg, _ = UnitOfMeasure.objects.get_or_create(code='kg', defaults={'description': 'Kilograms'})
        pcs, _ = UnitOfMeasure.objects.get_or_create(code='pcs', defaults={'description': 'Pieces'})
        ctn, _ = UnitOfMeasure.objects.get_or_create(code='ctn', defaults={'description': 'Cartons'})

        # 4. Product Categories
        fish, _ = ProductCategory.objects.get_or_create(name='Fish')
        shellfish, _ = ProductCategory.objects.get_or_create(name='Shellfish')
        crustaceans, _ = ProductCategory.objects.get_or_create(name='Crustaceans')

        # 5. Products
        products_data = [
            {'name': 'Tilapia (Whole)', 'category': fish, 'unit': kg},
            {'name': 'Nile Perch Fillet', 'category': fish, 'unit': kg},
            {'name': 'King Fish Steaks', 'category': fish, 'unit': kg},
            {'name': 'Red Snapper', 'category': fish, 'unit': kg},
            {'name': 'Lobster Tails', 'category': crustaceans, 'unit': kg},
            {'name': 'Tiger Prawns (Jumbo)', 'category': crustaceans, 'unit': kg},
            {'name': 'Calmari Rings', 'category': shellfish, 'unit': kg},
            {'name': 'Octopus (Tentacles)', 'category': shellfish, 'unit': kg},
        ]

        for p_data in products_data:
            p, created = Product.objects.get_or_create(name=p_data['name'], defaults={
                'category': p_data['category'],
                'unit': p_data['unit'],
                'description': f'Premium {p_data["name"]} sourced from the Indian Ocean.'
            })
            if created:
                self.stdout.write(f'Created product: {p.name}')

        # 6. Sample Shipments
        shipment, created = Shipment.objects.get_or_create(
            country_origin='Kenya',
            status='IN_TRANSIT',
            currency=usd,
            defaults={'id': uuid.uuid4()}
        )
        
        if created:
            # Add items to shipment
            ShipmentItem.objects.create(
                shipment=shipment,
                product=Product.objects.get(name='Tilapia (Whole)'),
                quantity=500,
                price_at_shipping=Decimal('4.50')
            )
            ShipmentItem.objects.create(
                shipment=shipment,
                product=Product.objects.get(name='Tiger Prawns (Jumbo)'),
                quantity=200,
                price_at_shipping=Decimal('18.00')
            )
            self.stdout.write(f'Created sample shipment: {shipment.id}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded SeaFood data'))
