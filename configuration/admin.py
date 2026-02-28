from django.contrib import admin
from .models import SystemParameter

@admin.register(SystemParameter)
class SystemParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'value', 'data_type', 'category', 'is_public', 'updated_at')
    list_filter = ('category', 'data_type', 'is_public')
    search_fields = ('name', 'key', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('General Info', {
            'fields': ('name', 'key', 'description', 'category')
        }),
        ('Setting Details', {
            'fields': ('value', 'data_type', 'is_public')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
