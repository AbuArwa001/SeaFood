from django.core.management.base import BaseCommand
from currencies.models import Currency
from currencies.utils import fetch_iso_currencies

class Command(BaseCommand):
    help = "Load ISO 4217 currencies from the internet"

    def handle(self, *args, **options):
        currencies = fetch_iso_currencies()
        for code, info in currencies.items():
            Currency.objects.get_or_create(
                code=code,
                defaults={"name": info["name"], "symbol": info["symbol"]},
            )
        self.stdout.write(self.style.SUCCESS("ISO 4217 currencies loaded successfully."))