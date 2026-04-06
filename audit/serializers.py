from rest_framework import serializers
from .models import ActivityLog
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'first_name', 'last_name']

class ActivityLogSerializer(serializers.ModelSerializer):
    user_details = UserSimpleSerializer(source='user', read_only=True)
    content_type_name = serializers.ReadOnlyField(source='content_type.model')
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_details', 'action', 'content_type', 
            'content_type_name', 'object_id', 'object_repr', 
            'details', 'ip_address', 'timestamp'
        ]
