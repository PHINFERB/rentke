from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'property_type', 'created_at')
    list_filter = ('property_type', 'city', 'has_parking')
    search_fields = ('title', 'description', 'address')
