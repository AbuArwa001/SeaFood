from rest_framework.test import APIClient
from users.models import User
import json

from django.conf import settings
print(f"REST_FRAMEWORK setting: {settings.REST_FRAMEWORK}")
try:

    user = User.objects.first()
    if not user:
        print("No users found. Creating a test user.")
        user = User.objects.create_user(username='testuser', password='testpassword')

    from currencies.views import CurrencyViewSet
    print(f"ViewSet pagination class: {CurrencyViewSet.pagination_class}")
    paginator = CurrencyViewSet.pagination_class()
    print(f"Paginator page_size: {paginator.page_size}")
    print(f"Paginator page_size_query_param: {paginator.page_size_query_param}")
    print(f"Paginator max_page_size: {paginator.max_page_size}")

    client = APIClient()
    client.force_authenticate(user=user)
    
    response = client.get('/api/v1/currencies/?page_size=10', HTTP_HOST='localhost')

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        count = len(results)
        print(f"Items returned: {count}")
        if count > 5:
            print("SUCCESS: Pagination page_size parameter is working.")
        else:
             print(f"FAILURE: Pagination page_size parameter NOT working. Returned {count} items.")
    else:
        print(f"Request failed: {response.content}")

except Exception as e:
    print(f"An error occurred: {e}")
