from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
import uuid


# --------------------
# Roles
# --------------------
class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.role_name

# --------------------
# UserManager
# --------------------
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, location, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            location=location,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, location, role, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email,
            full_name=full_name,
            location=location,
            role=role,
            password=password,
            **extra_fields
        )
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        if self.role and self.role.permissions.filter(
            codename=perm.split(".")[-1]
        ).exists():
            return True

        return False

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm) for perm in perm_list)
# --------------------
# Users
# --------------------
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users"
    )
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'location', 'role']

    def __str__(self):
        return self.full_name

