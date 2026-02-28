from django.db import models
import uuid

class ParameterType(models.TextChoices):
    TEXT = 'text', 'Text'
    BOOLEAN = 'boolean', 'Boolean'
    NUMBER = 'number', 'Number'
    JSON = 'json', 'JSON'

class ParameterCategory(models.TextChoices):
    GENERAL = 'general', 'General'
    FINANCIAL = 'financial', 'Financial'
    LOGISTICS = 'logistics', 'Logistics'
    NOTIFICATIONS = 'notifications', 'Notifications'
    SYSTEM = 'system', 'System'

class SystemParameter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    data_type = models.CharField(
        max_length=20, 
        choices=ParameterType.choices, 
        default=ParameterType.TEXT
    )
    category = models.CharField(
        max_length=20, 
        choices=ParameterCategory.choices, 
        default=ParameterCategory.GENERAL
    )
    is_public = models.BooleanField(default=True, help_text="Whether this parameter is visible to the frontend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "System Parameter"
        verbose_name_plural = "System Parameters"

    def __str__(self):
        return f"{self.name} ({self.key})"

    @classmethod
    def get_value(cls, key, default=None):
        try:
            param = cls.objects.get(key=key)
            if param.data_type == ParameterType.BOOLEAN:
                return param.value.lower() == 'true'
            elif param.data_type == ParameterType.NUMBER:
                try:
                    return float(param.value) if '.' in param.value else int(param.value)
                except ValueError:
                    return default
            elif param.data_type == ParameterType.JSON:
                import json
                try:
                    return json.loads(param.value)
                except json.JSONDecodeError:
                    return default
            return param.value
        except cls.DoesNotExist:
            return default
