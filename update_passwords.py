import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seafood.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User

# Generate password hash
password_hash = make_password('password321')
print(f"Password hash: {password_hash}")

# Update all users
updated = User.objects.all().update(password=password_hash)
print(f"Updated {updated} users with password 'password321'")
