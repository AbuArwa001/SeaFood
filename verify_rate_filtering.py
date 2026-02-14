from rest_framework.test import APIClient
from users.models import User
from exchangerates.models import ExchangeRate

try:
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='testuser', password='testpassword')

    client = APIClient()
    client.force_authenticate(user=user)

    # Get an existing exchange rate to use its currencies
    rate = ExchangeRate.objects.first()
    if not rate:
        print("No exchange rates found in DB.")
        exit(1)
    
    print(f"Testing with Rate: {rate.from_currency.code} -> {rate.to_currency.code}")

    # Test filtering by CODE
    url = f"/api/v1/exchange-rates/?from_currency__code={rate.from_currency.code}&to_currency__code={rate.to_currency.code}"
    print(f"Requesting: {url}")
    response = client.get(url, HTTP_HOST='localhost')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Results count (by code): {len(data.get('results', []))}")
    else:
        print(f"Error: {response.content}")

    # Test filtering by ID (might fail if not implemented)
    url_id = f"/api/v1/exchange-rates/?from_currency={rate.from_currency.id}&to_currency={rate.to_currency.id}"
    print(f"Requesting: {url_id}")
    response_id = client.get(url_id, HTTP_HOST='localhost')
    print(f"Status: {response_id.status_code}")
    if response_id.status_code == 200:
        data = response_id.json()
        print(f"Results count (by ID): {len(data.get('results', []))}")
    else:
        print(f"Error: {response_id.content}")

except Exception as e:
    print(f"Exception: {e}")
