from django.contrib import admin
from .models import Property
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'property_type', 'created_at')
    list_filter = ('property_type', 'city', 'has_parking')
    search_fields = ('title', 'description', 'address')
