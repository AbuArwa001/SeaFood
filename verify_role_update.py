from rest_framework.test import APIClient
from users.models import User, Role
import json

try:
    # 1. Setup Admin User
    admin_role, _ = Role.objects.get_or_create(role_name="Admin")
    admin_user = User.objects.filter(role=admin_role).first()
    if not admin_user:
        admin_user = User.objects.create_user(
            email="admin@test.com", 
            password="adminpassword", 
            full_name="Admin User", 
            location="HQ", 
            role=admin_role
        )
        print("Created Admin User")

    # 2. Setup Target User
    staff_role, _ = Role.objects.get_or_create(role_name="Staff")
    target_user = User.objects.filter(role=staff_role).first()
    if not target_user:
        target_user = User.objects.create_user(
            email="staff@test.com", 
            password="staffpassword", 
            full_name="Staff User", 
            location="Branch", 
            role=staff_role
        )
        print("Created Target User")
        
    print(f"Target User Initial Role: {target_user.role.role_name}")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 3. Attempt to update role to Admin
    url = f"/api/v1/users/{target_user.id}/"
    payload = {
        "role_id": str(admin_role.id)
    }
    
    print(f"Attrng to update user {target_user.id} to role {admin_role.role_name} ({admin_role.id})")
    
    response = client.patch(url, data=payload, format='json', HTTP_HOST='localhost')
    
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        target_user.refresh_from_db()
        print(f"Target User New Role: {target_user.role.role_name}")
        if target_user.role.role_name == "Admin":
            print("SUCCESS: Role updated to Admin.")
        else:
            print("FAILURE: Role did not update.")
    else:
        print(f"FAILURE: {response.content}")

except Exception as e:
    print(f"Exception: {e}")
