from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def get_permissions_for_models(model_labels, actions=None):
    """
    model_labels: list like ["costs.CostLedger", "shipments.Shipment"]
    actions: list like ["view", "add", "change", "delete"]
    """

    if actions is None:
        actions = ["view", "add", "change"]

    permissions = Permission.objects.none()

    for label in model_labels:
        app_label, model_name = label.split(".")

        content_type = ContentType.objects.get(
            app_label=app_label,
            model=model_name.lower()
        )

        perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=[f"{action}_{model_name.lower()}" for action in actions]
        )

        permissions |= perms

    return permissions
