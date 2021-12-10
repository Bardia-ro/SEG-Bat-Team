from typing import ClassVar
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import BLANK_CHOICE_DASH, proxy
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
from location_field.models.plain import PlainLocationField
from libgravatar import Gravatar
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
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
        return Tournaments.objects.filter(club=self)

class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

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
        return self.user.email

    def approve_membership(self):
        self.role = Role.MEMBER
        self.save()

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


class Tournaments(models.Model):

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
    #number_of_contenders = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(2), MaxValueValidator(capacity)])
    deadline = models.DateTimeField(blank=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    contender = models.ManyToManyField(User, related_name = '+')

    def __str__(self):
        return self.name

    def is_contender(self,user_id):
        """Returns whether a user is a contender in this tournament"""
        user = User.objects.get(id=user_id)
        return user in self.contender.all()

    def contender_count(self):
        """ Returns the number of contenders in this tournament"""
        return self.contender.count()

    def is_space(self):
        """Returns whether this tournament has space for more contenders"""
        return  (self.contender.count() < self.capacity)

    def is_time_left(self):
        """Returns whether there is time to apply to this tournament"""
        current_time = timezone.now()
        return (current_time < self.deadline)

    def toggle_apply(self, user_id):
        """ Toggles whether a user has applied to this tournament"""
        user = User.objects.get(id=user_id)
        if self.is_time_left():
            if self.is_contender(user_id):
                    self.contender.remove(user)
            else:
                if self.is_space():
                        self.contender.add(user)

class Match(models.Model):
    number = models.PositiveSmallIntegerField()
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'player2')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner')

class EliminationStages(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)

    PLAYER_NUMBER_CHOICES = [
        (2, 2),
        (4, 4),
        (8, 8),
        (16, 16)
    ]
    number_of_players = models.PositiveSmallIntegerField(choices=PLAYER_NUMBER_CHOICES)
    

# ROUND_CHOICES = [
#         (2, 'Final'),
#         (4, 'Semi-final'),
#         (8, 'Quarter-final'),
#         (16, 'Round-of-sixteen')
#     ]

# elimination_round = models.CharField(choices=ROUND_CHOICES)

class EliminationMatch(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    elimination_stages = models.ForeignKey(EliminationStages, on_delete=models.CASCADE)