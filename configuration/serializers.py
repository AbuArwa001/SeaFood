from rest_framework import serializers
from .models import SystemParameter

class SystemParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemParameter
        fields = [
            'id', 
            'name', 
            'key', 
            'value', 
            'description', 
            'data_type', 
            'category', 
            'is_public', 
            'updated_at'
        ]
        read_only_fields = ['id', 'key', 'updated_at']
