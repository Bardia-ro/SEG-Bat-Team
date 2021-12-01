"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, User, Club

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'first_name', 'last_name', 'email', 'is_active',
    ]
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Config"""
    list_display = [
        'user', 'club'
    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Config"""
    list_display = [
        'name', 'location', 'description'
    ]