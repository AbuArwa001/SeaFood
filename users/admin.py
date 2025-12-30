from django.contrib import admin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "role", "is_staff")
    search_fields = ("email", "full_name")

