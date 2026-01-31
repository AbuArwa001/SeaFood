import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seafood.settings')
django.setup()

from users.models import User

def reset_passwords():
    users = User.objects.all()
    count = 0
    for user in users:
        user.set_password('password123')
        user.save()
        count += 1
    
    print(f"Successfully reset passwords for {count} users to 'password123'")

if __name__ == '__main__':
    reset_passwords()
