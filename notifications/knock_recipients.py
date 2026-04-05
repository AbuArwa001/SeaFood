"""
Helper to build Knock recipient lists for role-based in-app notifications.
"""

NOTIFY_ROLES = ("Super Admin", "Admin", "Finance Agent", "Sales Agent")


def get_role_recipients(extra_roles=None):
    """
    Returns a list of user ID strings for all active users in NOTIFY_ROLES
    (plus any extra_roles passed in). Safe to call from any Django context.
    """
    from users.models import User

    roles = list(NOTIFY_ROLES) + (list(extra_roles) if extra_roles else [])
    ids = User.objects.filter(
        role__role_name__in=roles,
        is_active=True,
    ).values_list("id", flat=True)
    return [str(uid) for uid in ids]
