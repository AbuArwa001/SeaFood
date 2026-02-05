import os
import django
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seafood.settings')
django.setup()

User = get_user_model()

def test_user_permissions():
    users = [
        ('admin@seafood.com', 'Admin'),
        ('sales@seafood.com', 'Sales Agent'),
        ('viewer@seafood.com', 'Viewer')
    ]

    client = APIClient()

    for email, role_name in users:
        print(f"\n--- Testing User: {email} ({role_name}) ---")
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.email}, Role: {user.role.role_name}")
        except User.DoesNotExist:
            print(f"ERROR: User {email} not found!")
            continue

        # Authenticate
        refresh = client.post('/api/v1/token/', {'email': email, 'password': 'password123'}, format='json')
        if refresh.status_code == 200:
             token = refresh.data['access']
             client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
             print("Login successful, token obtained.")
             
             # Try to access a protected endpoint (e.g., users list)
             response = client.get('/api/v1/users/')
             print(f"Accessing /api/v1/users/: Status {response.status_code}")
             if response.status_code == 403:
                 print("FORBIDDEN: Checking permissions logic...")
                 # Manually check permissions logic
                 from users.permissions import CanCreateUser, IsAdmin
                 request = type('Request', (object,), {'user': user, 'is_authenticated': True})
                 perm = IsAdmin() # Assuming the endpoint uses a permission like this
                 print(f"IsAdmin check: {perm.has_permission(request, None)}")
                 
        else:
            print(f"Login FAILED: {refresh.status_code} {refresh.data}")

if __name__ == '__main__':
    test_user_permissions()
