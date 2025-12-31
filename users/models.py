from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
import uuid


# --------------------
# Roles
# --------------------
class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles"
    )
    def __str__(self):
        return self.role_name

# --------------------
# UserManager
# --------------------
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, location, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, location=location, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, location, role, password):
        user = self.create_user(email, full_name, location, role, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


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
    location = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            self.user_permissions.set(self.role.permissions.all())

