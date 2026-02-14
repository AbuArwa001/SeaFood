from rest_framework.test import APIClient
from users.models import User
from exchangerates.models import ExchangeRate
import random

try:
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='testuser', password='testpassword')

    client = APIClient()
    client.force_authenticate(user=user)

    # Get a random exchange rate to test with
    count = ExchangeRate.objects.count()
    if count == 0:
        print("No exchange rates found.")
        exit(1)
        
    random_index = random.randint(0, count - 1)
    rate = ExchangeRate.objects.all()[random_index]
    
    from_code = rate.from_currency.code
    to_code = rate.to_currency.code
    
    print(f"Testing Specific Fetch: {from_code} -> {to_code}")

    # 1. Test Direct Fetch
    url = f"/api/v1/exchange-rates/?from_currency__code={from_code}&to_currency__code={to_code}"
    print(f"Requesting Direct: {url}")
    response = client.get(url, HTTP_HOST='localhost')
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if len(results) > 0:
            print(f"SUCCESS: Found {len(results)} rates directly.")
            print(f"Rate: {results[0]['rate']}")
        else:
            print("FAILURE: No rates found directly.")
    else:
        print(f"FAILURE: API Error {response.status_code}")

    # 2. Test Inverse Fetch (Simulated)
    # in real usage, we'd swap codes, but here we just check if the API accepts the params
    url_inverse = f"/api/v1/exchange-rates/?from_currency__code={to_code}&to_currency__code={from_code}"
    print(f"Requesting Inverse: {url_inverse}")
    response_inv = client.get(url_inverse, HTTP_HOST='localhost')
    
    if response_inv.status_code == 200:
        data = response_inv.json()
        results = data.get('results', [])
        # It's okay if this is empty if the inverse doesn't exist, 
        # but the request itself should succeed
        print(f"Inverse Request Status: OK. Found {len(results)} rates.")
    else:
         print(f"FAILURE: API Error on inverse request {response_inv.status_code}")

except Exception as e:
    print(f"Exception: {e}")
