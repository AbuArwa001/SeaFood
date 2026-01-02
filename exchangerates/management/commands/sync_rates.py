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
        BASE_CURR_CODE = "KES"
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURR_CODE}"

        try:
            # 2. Fetch Data
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            rates = data.get("conversion_rates", {})
            rate_date = timezone.now().date()

            # 3. Get Base Currency Instance
            try:
                base_currency = Currency.objects.get(code=BASE_CURR_CODE)
            except Currency.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Base currency {BASE_CURR_CODE} not found in DB!"))
                return

            # 4. Save to Database (using a transaction for safety)
            count = 0
            with transaction.atomic():
                for code, rate_value in rates.items():
                    # Skip if it's the same currency (handled by your model.clean())
                    if code == BASE_CURR_CODE:
                        continue
                    
                    # Only save if the target currency exists in our system
                    target_currency = Currency.objects.filter(code=code).first()
                    
                    if target_currency:
                        # update_or_create handles the unique_together constraint
                        obj, created = ExchangeRate.objects.update_or_create(
                            from_currency=base_currency,
                            to_currency=target_currency,
                            rate_date=rate_date,
                            defaults={'rate': rate_value}
                        )
                        if created:
                            count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully saved {count} new rates for {rate_date}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to sync rates: {str(e)}"))