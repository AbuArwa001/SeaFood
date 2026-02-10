import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from currencies.models import Currency
from exchangerates.models import ExchangeRate

class Command(BaseCommand):
    help = "Fetches daily rates from ExchangeRate-API and saves to DB"

    def handle(self, *args, **options):
        # 1. Configuration
        API_KEY = "9808e08a988476b896211098"
        # We'll use USD as the primary pivot currency to get global rates
        PRIMARY_BASE = "USD"
        rate_date = timezone.now().date()
        
        active_currencies = Currency.objects.filter(is_active=True)
        if not active_currencies.exists():
            self.stdout.write(self.style.WARNING("No active currencies found in database."))
            return

        # 2. Identify if we want to sync starting from multiple bases or just USD
        # For small sets, fetching USD and calculating cross-rates is efficient.
        # However, to keep it simple and direct for the user, we'll fetch rates based on what's active.
        
        bases_to_fetch = [PRIMARY_BASE]
        # If USD isn't in our DB, use the first active currency as backup
        if not active_currencies.filter(code=PRIMARY_BASE).exists():
            bases_to_fetch = [active_currencies.first().code]

        total_count = 0
        for base_code in bases_to_fetch:
            self.stdout.write(f"Fetching rates with base: {base_code}...")
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_code}"
            
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                if data.get("result") != "success":
                    self.stderr.write(self.style.ERROR(f"API Error for {base_code}: {data.get('error-type')}"))
                    continue

                conversion_rates = data.get("conversion_rates", {})
                base_currency = Currency.objects.get(code=base_code)

                with transaction.atomic():
                    for target_code, rate_value in conversion_rates.items():
                        if target_code == base_code:
                            continue
                        
                        target_currency = active_currencies.filter(code=target_code).first()
                        if target_currency:
                            obj, created = ExchangeRate.objects.update_or_create(
                                from_currency=base_currency,
                                to_currency=target_currency,
                                rate_date=rate_date,
                                defaults={'rate': rate_value}
                            )
                            if created:
                                total_count += 1
                
                self.stdout.write(self.style.SUCCESS(f"Finished syncing for {base_code}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to sync for {base_code}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Global sync complete. {total_count} new rate(s) saved for {rate_date}"))