"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Elo_Rating, Match, Tournament, User, UserInClub, Club, EliminationMatch, Group, GroupMatch, GroupMatchNextMatches, GroupPoints


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'first_name', 'last_name', 'email', 'is_active'
    ]

@admin.register(UserInClub)
class UserInClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for roles."""

    list_display = [
        'user', 'club', 'role'

    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'location', 'description'
    ]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Matches."""

    list_display = [
        'number', 'player1', 'player2'
    ]

@admin.register(Elo_Rating)
class EloRatingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Elo rating."""

    list_display = [
        'user', 'rating', 'club','result'
    ]

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Tournaments."""

    list_display = [
        'name', 'description', 'capacity','deadline', 'club', 'organiser' , 'current_stage'
    ]

@admin.register(EliminationMatch)
class EliminationMatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Matches."""

    list_display = [
        'tournament', 'match', 'winner','winner_next_match'
    ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Groups."""

    list_display = [
        'number', 'group_stage'
    ]

@admin.register(GroupMatch)
class GroupMatchAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Group matches."""

    list_display = [
        'match', 'group', 'player1_points', 'player2_points', 'display'
    ]

@admin.register(GroupMatchNextMatches)
class GroupMatchNextMatchesAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Group match next matches."""

    list_display = [
        'group_match'
    ]

@admin.register(GroupPoints)
class GroupPointsAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Group points."""

    list_display = [
        'group', 'player', 'total_group_points'
    ]






