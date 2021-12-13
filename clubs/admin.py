"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Elo_Rating, Match, Tournament, User, Role, Club


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

@admin.register(Tournament)
class TournamentsAdmin(admin.ModelAdmin):
     """Configuration of the admin interface for Tournaments."""
     exclude = ['contender',]

     list_display = [
        'name', 'description', 'club', 'capacity', 'organiser', 'deadline',
    ]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Matches."""

    list_display = [
        'number', 'player1', 'player2'
    ]

@admin.register(Elo_Rating)
class EloRatingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Matches."""

    list_display = [
        'user', 'rating', 'club'
    ]
