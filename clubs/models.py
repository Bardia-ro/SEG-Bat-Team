"""Models in the clubs app."""
from typing import ClassVar
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import BLANK_CHOICE_DASH, NullBooleanField, proxy
from django.db.models.query import QuerySet
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.shortcuts import get_object_or_404
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
from location_field.models.plain import PlainLocationField
from libgravatar import Gravatar
from django.utils import timezone, tree


class User(AbstractBaseUser, PermissionsMixin):
    """User model used for authentication and creating clubs"""
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    experience = models.CharField(max_length=520, blank=False)
    personal_statement = models.CharField(max_length=600, blank=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='identicon')
        return gravatar_url


    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def get_first_club_id_user_is_associated_with(self):
        club = Club.objects.filter(users__id = self.id).first()
        if club == None:
            return 0
        else:
            return club.id

    def get_role_at_club(self, club_id):
        return Role.objects.get(club__id=club_id, user__id=self.id).role

    def get_role_as_text_at_club(self, club_id):
        try:
            role = Role.objects.get(club_id=club_id, user=self).role
        except:
            return "Not a member"
        if role == 2:
            return "Member"
        elif role == 3:
            return "Officer"
        elif role == 4:
            return "Owner"
        elif role== 1:
            return "Application Pending"


    def get_is_user_associated_with_club(self, club_id):
        try:
            Role.objects.get(club__id=club_id, user__id=self.id)
            return True
        except Role.DoesNotExist:
            return False

    def get_clubs_user_is_a_member(self):
        as_member = Role.objects.filter(role=2, user=self)
        as_officer = Role.objects.filter(role=3, user=self)
        as_owner = Role.objects.filter(role=4, user=self)
        return as_member.union(as_officer,as_owner)

class Club(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    city = models.CharField(max_length =255)
    location = PlainLocationField(based_fields = ['city'], zoom = 7)
    description = models.CharField(max_length=600, blank=False)
    users = models.ManyToManyField(User, through='Role')

    def __str__(self):
        return self.name

    def get_total(self):
        the_members = Role.objects.filter(club=self, role=2)
        the_officers = Role.objects.filter (club=self, role=3)
        the_owner = Role.objects.filter(club=self, role=4)
        return the_officers.union(the_members,the_owner).count()

    def get_owner(self):
        return Role.objects.get(club=self, role=4).user

    def get_officers(self):
        return Role.objects.filter(club=self, role=3)

    def get_members(self):
        return Role.objects.filter(club=self, role=2)

    def get_tournaments(self):
        return Tournament.objects.filter(club=self)

class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    elo_rating = models.IntegerField(blank=False, default=1000)

    NO_CLUB = 0
    APPlICANT = 1
    MEMBER = 2
    OFFICER = 3
    OWNER = 4

    ROLE_CHOICES = (
        (NO_CLUB, 'No_club',),
        (APPlICANT, 'Applicant'),
        (MEMBER, 'Member'),
        (OFFICER, 'Officer'),
        (OWNER, 'Owner'),
    )

    role = models.SmallIntegerField(
        blank=False, default=APPlICANT, choices=ROLE_CHOICES)

    def role_name(self):
        if self.role == Role.APPlICANT:
           return "Applicant"
        elif self.role == Role.MEMBER:
            return "Member"
        elif self.role == Role.OFFICER:
            return "Officer"
        elif self.role == Role.OWNER:
            return "Owner"

    def user_email(self):
        return self.user.first_name

    def approve_membership(self):
        self.role = Role.MEMBER
        self.save()

    def reject_membership(self):
        self.delete()

    def promote_member_to_officer(self):
        self.role = Role.OFFICER
        self.save()

    def demote_officer_to_member(self):
        self.role = Role.MEMBER
        self.save()

    def demote_member_to_applicant(self):
        self.role = Role.APPlICANT
        self.save()

    def change_owner(self, club_id, new_owner_id):
        self.role = Role.OFFICER
        self.save()
        new_owner_role_instance = Role.objects.get(club_id=club_id, user_id=new_owner_id)
        new_owner_role_instance.role = Role.OWNER
        new_owner_role_instance.save()

    def is_owner(self):
        return self.role == 4

    def is_member(self):
        return self.role == 2

    def is_applicant(self):
        return self.role == 1

    def is_officer(self):
        return self.role == 3

    def is_user_member_or_above(self):
        return self.role > 1

    def get_Officers(self):
        officers = Role.objects.all().filter(role = 3)
        return officers

    def adjust_elo_rating(self, match, club_id, winner):
        player_1 = match.match.player1
        player_2 = match.match.player2

        p1 = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = player_1.id)
        p2 = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = player_2.id)

        tup = self.calculate_expected_scores(player_1, player_2, club_id, winner)
        p1.elo_rating = tup[0]
        p2.elo_rating = tup[1]
        p1.save()
        p2.save()
        if (winner != "Draw"):
            Elo_Rating.objects.create(
                    result = winner,
                    user = player_1,
                    match = match.match,
                    rating = tup[0],
                    club_id = club_id
                )
            Elo_Rating.objects.create(
                    result = winner,
                    user = player_2,
                    match = match.match,
                    rating = tup[1],
                    club_id = club_id
                )
        else:
            Elo_Rating.objects.create(
                    user = player_1,
                    match = match.match,
                    rating = tup[0],
                    club_id = club_id
                )
            Elo_Rating.objects.create(
                    user = player_2,
                    match = match.match,
                    rating = tup[1],
                    club_id = club_id
                )


    def calculate_expected_scores(self, player_1, player_2, club_id,winner):
        p1 = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = player_1.id)
        p2 = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = player_2.id)
        elo_A = p1.elo_rating
        elo_B = p2.elo_rating
        res_A = 1
        res_B = 1
        divA = (elo_B - elo_A)/400
        divA_ = (10**divA) + 1
        E_A = 1/divA_

        divB = (elo_A - elo_B)/400
        divB_ = (10**divB) + 1
        E_B = 1/divB_
        if winner == player_1:
            res_A = 1
            res_B = 0
        elif winner == player_2:
            res_A = 0
            res_B = 1
        elif winner == "Draw":
            print("called")
            res_A = 0.5
            res_B = 0.5

        new_elo_A = elo_A + 32 * (res_A - E_A)
        new_elo_B = elo_B + 32 * (res_B - E_B)

        return new_elo_A , new_elo_B



class Tournament(models.Model):

    TWO = 2
    FOUR = 4
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32
    SIXTY_FOUR = 64

    CAPACITY_CHOICES = (
        (TWO, 'Two',),
        (FOUR, 'Four'),
        (EIGHT, 'Eight'),
        (SIXTEEN, 'Sixteen'),
        (THIRTY_TWO, 'Thirty_Two'),
        (SIXTY_FOUR, 'Sixty_Four'),
    )

    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.CharField(max_length=600, blank=False)
    capacity = models.SmallIntegerField(
        blank=False, choices=CAPACITY_CHOICES)
    deadline = models.DateTimeField(blank=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name = '+')

    STAGE_CHOICES = [
        ('F', 'Finished'),
        ('E', 'Elimination rounds'),
        ('G32', 'Group stage'),
        ('G96', 'Group stage'),
        ('S', 'Start'),
    ]

    current_stage = models.CharField(max_length = 3, choices = STAGE_CHOICES, default = 'S')

    def __str__(self):
        return self.name

    def is_player(self,user_id):
        """Returns whether a user is a player in this tournament"""
        user = User.objects.get(id=user_id)
        return user in self.players.all()

    def player_count(self):
        """ Returns the number of players in this tournament"""
        return self.players.count()

    def is_space(self):
        """Returns whether this tournament has space for more players"""
        return  (self.players.count() < self.capacity)

    def is_time_left(self):
        """Returns whether there is time to apply to this tournament"""
        current_time = timezone.now()
        return (current_time < self.deadline)

    def toggle_apply(self, user_id):
        """ Toggles whether a user has applied to this tournament"""
        user = User.objects.get(id=user_id)
        if self.is_time_left():
            if self.is_player(user_id):
                    self.players.remove(user)
            else:
                if self.is_space():
                        self.players.add(user)

    def remove_player(self, user_id):
        """Removes a player from a tournament"""
        user = User.objects.get(id=user_id)
        self.players.remove(user)

    def valid_player_count(self):
        valid_numbers = [2,4,8,16,24,32,48,64,80,96]
        capacity = self.players.count()
        return(capacity in valid_numbers)

    def generate_next_matches(self):
        """Create the next matches that should be created in this tournament"""

        players = self.players.all()
        num_players = self.player_count()

        if self.current_stage == 'S':
            self._set_current_stage_to_first_stage(num_players)

        if self.current_stage == 'G96':
            self._generate_group_stage_for_96_people_or_less(players, num_players)
        elif self.current_stage == 'G32':
            return self._generate_group_stage_for_32_people_or_less(players, num_players)
        elif self.current_stage == 'E':
            return self._create_elimination_matches(players, num_players)

    def _set_current_stage_to_first_stage(self, num_players):
        """Set this tournament's current_stage field to the first stage for this tournament"""

        if num_players > 32 and num_players <= 96:
            self.current_stage = 'G96'
        elif num_players > 16 and num_players <= 32:
            self.current_stage = 'G32'
        else:
            self.current_stage = 'E'

        self.save()

    def _generate_group_stage_for_96_people_or_less(self, players, num_players):
        """Generate group stage if the number of players is between 17 and 32"""

        self.current_stage = 'G32'
        self.save()

        if num_players == 64:
            num_players_per_group = 4
            for i in range(0, num_players, num_players_per_group):
                self._create_group(i, players, num_players_per_group, 'G96')

    def _generate_group_stage_for_32_people_or_less(self, players, num_players):
        """Generate group stage if the number of players is between 17 and 32"""

        if num_players <= 32:
            group_round_players = players
        elif num_players > 32:#check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            groups = Group.objects.filter(
                tournament = self,
                group_stage = 'G96'
            )

            for group in groups:
                group_matches = GroupMatch.objects.filter(group=group)
                for group_match in group_matches:
                    if group_match.player1_points == 0 and group_match.player2_points == 0:
                        return 'All group match results must be submitted before generating next group stage matches'

            group_round_players = list(players[0: 32])
            for group in groups:
                group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
                if group.number % 2 == 1:
                    group_round_players[group.number-1] = group_points_objects[0].player
                    group_round_players[group.number+16-1] = group_points_objects[1].player
                elif group.number % 2 == 0:
                    group_round_players[group.number-1] = group_points_objects[1].player
                    group_round_players[group.number+16-1] = group_points_objects[0].player

        num_players_group_round = len(group_round_players)

        self.current_stage = 'E'
        self.save()

        if num_players_group_round == 32:
            num_players_per_group = 4
            for i in range(0, 32, num_players_per_group):
                self._create_group(i, group_round_players, num_players_per_group, 'G32')

    def _create_group(self, i, players, num_players_per_group, group_stage):
        """Create a group for a group stage"""

        group_players = players[i: i+num_players_per_group]
        group = Group.objects.create(
            number = int(i / num_players_per_group) + 1,
            tournament = self,
            group_stage = group_stage
        )
        group.players.set(group_players)

        for i in range(num_players_per_group):
            self._set_group_player_points(group, group_players[i])

        self._generate_group_matches(group, group_players, num_players_per_group)

    def _set_group_player_points(self, group, player):
        """Create a GroupPoint instance for a player in a group"""

        GroupPoints.objects.create(
            group = group,
            player = player
        )

    def _generate_group_matches(self, group, group_players, num_players_per_group):
        for i in range(num_players_per_group-1):
            for j in range(i+1, num_players_per_group):
                match = Match.objects.create(
                    player1 = group_players[i],
                    player2 = group_players[j]
                )

                GroupMatch.objects.create(
                    match = match,
                    group = group,
                )

        group_matches = GroupMatch.objects.filter(group=group)
        group_match_count = group_matches.count()
        odd_match_number = 1
        if group_match_count % 2 == 1:
            even_match_number = group_match_count - 1
        else:
            even_match_number = group_match_count
        num_players_per_group_divided_by_two = int(num_players_per_group/2)
        for i in range(group_match_count):
            group_match = group_matches[i].match
            if i < int(group_match_count/2):
                group_match.number = odd_match_number
                odd_match_number += num_players_per_group_divided_by_two
                group_match.save()
            else:
                group_match.number = even_match_number
                even_match_number -= num_players_per_group_divided_by_two
                group_match.save()


        for group_match in group_matches:
            match_number = group_match.match.number

            if match_number <= num_players_per_group_divided_by_two:
                group_match.display = True
                group_match.save()

            if match_number % 2 == 1:
                adjusted_for_oddness_match_number = match_number + 1
            else:
                adjusted_for_oddness_match_number = match_number

            next_matches = GroupMatch.objects.filter(
                group=group,
                match__number__gt = adjusted_for_oddness_match_number,
                match__number__lt = adjusted_for_oddness_match_number + num_players_per_group_divided_by_two + 1
            )

            group_match_next_matches_instance = GroupMatchNextMatches.objects.create(
                group_match = group_match
            )
            group_match_next_matches_instance.next_matches.set(next_matches)

    def _create_elimination_matches(self, players, num_players):
        if num_players <= 16:
            elim_rounds_players = players
        elif num_players > 16:#check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            groups = Group.objects.filter(
                tournament = self,
                group_stage = 'G32'
            )

            for group in groups:
                group_matches = GroupMatch.objects.filter(group=group)
                for group_match in group_matches:
                    if group_match.player1_points == 0 and group_match.player2_points == 0:
                        return 'All group match results must be submitted before generating elimination rounds matches'

            elim_rounds_players = list(players[0: 16])
            for group in groups:
                group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
                if group.number % 2 == 1:
                    elim_rounds_players[group.number-1] = group_points_objects[0].player
                    elim_rounds_players[group.number+8-1] = group_points_objects[1].player
                elif group.number % 2 == 0:
                    elim_rounds_players[group.number-1] = group_points_objects[1].player
                    elim_rounds_players[group.number+8-1] = group_points_objects[0].player

        num_players_elim = len(elim_rounds_players)

        self.current_stage = 'F'
        self.save()

        if num_players_elim == 2:
            self._create_elimination_matches_for_two_players(elim_rounds_players)
        elif num_players_elim == 4 or num_players_elim == 8 or num_players_elim == 16:
            match = Match.objects.create(number = num_players_elim-1)
            EliminationMatch.objects.create(
                tournament = self,
                match = match
            )

            for n in range(num_players_elim-2, int(num_players_elim/2), -1):
                match = Match.objects.create(number = n)
                self._create_elimination_match_with_non_null_winner_next_match_field(n, match, num_players_elim)

            for n in range(1, (int(num_players_elim/2))+1):
                match = Match.objects.create(
                    number = n,
                    player1 = elim_rounds_players[2*n-2],
                    player2 = elim_rounds_players[2*n-1]
                )

                self._create_elimination_match_with_non_null_winner_next_match_field(n, match, num_players_elim)

    def _create_elimination_matches_for_two_players(self, elim_rounds_players):
        match = Match.objects.create(
            number = 1,
            player1 = elim_rounds_players[0],
            player2 = elim_rounds_players[1]
        )

        EliminationMatch.objects.create(
            tournament = self,
            match = match
        )

    def _create_elimination_match_with_non_null_winner_next_match_field(self, n, match, num_players_elim):
        if n % 2 == 1:
            adjusted_for_oddness_n = n + 1
        else:
            adjusted_for_oddness_n = n

        EliminationMatch.objects.create(
            tournament = self,
            match = match,
            winner_next_match = EliminationMatch.objects.get(
                tournament = self,
                match__number = int(adjusted_for_oddness_n/2) + int(num_players_elim/2)
            ).match
        )

class Match(models.Model):
    """Model representing a basic match"""

    number = models.PositiveSmallIntegerField(null=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name= '+')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name= '+')

class EliminationMatch(models.Model):
    """Model representing an elimination match"""

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')
    winner_next_match = models.ForeignKey(Match, null=True, on_delete=models.CASCADE, related_name = '+')

    def set_winner(self, player):
        """Sets the winner for this match"""
        self.winner = player
        self.save()
        self.set_winner_as_player_in_winner_next_match()

    def set_winner_as_player_in_winner_next_match(self):
        """Set the winner of this match as a player in their next match if they have a next match"""

        if self.winner_next_match:
            if self.match.number % 2 == 1:
                self.winner_next_match.player1 = self.winner
            else:
                self.winner_next_match.player2 = self.winner

            self.winner_next_match.save()

class Elo_Rating(models.Model):
    result = models.ForeignKey(User, on_delete=models.CASCADE,null=True ,related_name='+')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, default=1000)


class Group(models.Model):
    """Model representing a group"""

    number = models.PositiveSmallIntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)

    GROUP_STAGE = [
        ('G32', 'Group stage'),
        ('G96', 'Group stage'),
    ]

    group_stage = models.CharField(max_length = 3, choices = GROUP_STAGE)

    def get_group_groupmatches(self):
        """Return the group matches in this group"""

        return GroupMatch.objects.filter(group=self).order_by('match__number')

    def get_group_grouppoints(self):
        """Return the GroupPoints objects associated with this group"""

        return GroupPoints.objects.filter(group=self).order_by('-total_group_points')

class GroupMatch(models.Model):
    """Model representing a group match"""

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'group')
    player1_points = models.FloatField(default = 0)
    player2_points = models.FloatField(default = 0)
    display = models.BooleanField(default = False)

    def player1_won_points(self):
        """Set the score of player 1"""
        self.player1_points += 1
        self.save()

        self._update_player1_total_group_points(1)

        self._show_next_group_matches_in_match_schedule()

    def player2_won_points(self):
        """Set the score of player 2"""
        self.player2_points += 1
        self.save()

        self._update_player2_total_group_points(1)

        self._show_next_group_matches_in_match_schedule()

    def set_draw_points(self):
        """Updates the score if the match is a draw"""
        self.player1_points += 0.5
        self.player2_points += 0.5
        self.save()

        self._update_player1_total_group_points(0.5)

        self._update_player2_total_group_points(0.5)

        self._show_next_group_matches_in_match_schedule()

    def _get_group_points_object_for_player1(self):
        """Return GroupPoints object for player1 in the group that this group match is part of"""

        return GroupPoints.objects.get(
            group=self.group,
            player=self.match.player1
        )

    def _get_group_points_object_for_player2(self):
        """Return GroupPoints object for player2 in the group that this group match is part of"""

        return GroupPoints.objects.get(
            group=self.group,
            player=self.match.player2
        )

    def _update_player1_total_group_points(self, points):
        """Update player1 total group points"""

        group_points_for_player1 = self._get_group_points_object_for_player1()
        group_points_for_player1.total_group_points += points
        group_points_for_player1.save()

    def _update_player2_total_group_points(self, points):
        """Update player2 total group points"""

        group_points_for_player2 = self._get_group_points_object_for_player2()
        group_points_for_player2.total_group_points += points
        group_points_for_player2.save()

    def _show_next_group_matches_in_match_schedule(self):
        """Set the display field of the next matches that should be displayed after the result of this group match has been submitted to True"""

        group_match_next_matches_object = GroupMatchNextMatches.objects.get(group_match=self)
        for group_match in group_match_next_matches_object.next_matches.all():
            group_match.display = True
            group_match.save()

class GroupMatchNextMatches(models.Model):
    """Model to hold the next group matches that should be displayed after the result for a group match has been submitted"""

    group_match = models.ForeignKey(GroupMatch, on_delete=models.CASCADE)
    next_matches = models.ManyToManyField(GroupMatch, related_name='+')

class GroupPoints(models.Model):
    """Model to hold the total points a player has in a group in a group stage"""

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='winner')
    total_group_points = models.FloatField(default=0)
