"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Match, MatchResult, Tournaments, User, Role, Club


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for roles."""

    list_display = [
        'user', 'club', 'role'

    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'location', 'description', 
    ]

@admin.register(Tournaments)
class TournamentsAdmin(admin.ModelAdmin):
     """Configuration of the admin interface for Tournaments."""

     list_display = [
        'name', 'description', 'club', 'capacity', 'organiser', 'deadline',
    ]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Matches."""

    list_display = [
        'tournament', 'participant_one', 'participant_two',
    ]

@admin.register(MatchResult)
class ResultMatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Match result."""

    list_display = [
        'match' ,'winner', 'loser',
    ]