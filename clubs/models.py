from django.core.validators import RegexValidator
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


class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    BANNED = 0
    APPlICANT = 1
    MEMBER = 2
    OFFICER = 3
    OWNER = 4

    ROLE_CHOICES = (
        (BANNED, 'Banned',),
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
