from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User

@receiver(post_save, sender=User)
def assign_role_permissions(sender, instance, created, **kwargs):
    if created and instance.role:
        instance.user_permissions.set(instance.role.permissions.all())
        