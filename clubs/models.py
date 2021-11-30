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
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()
        return 'http://www.gravatar.com/avatar/{}'.format(digest)

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def approve_membership(self):
        self.role = User.MEMBER
        self.save()
    
    def get_first_club_id_user_is_associated_with(self):
        id = Club.objects.filter(users__id = self.id).first().id
        if id == None:
            return -1
        else:
            return id

    def get_role_at_club(self, club_id):
        return Role.objects.get(club__id=club_id, user__id=self.id).role

class Club(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    location = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=600, blank=False)

    users = models.ManyToManyField(User, through='Role')

class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    BANNED = 0
    APPlICANT = 1
    MEMBER = 2
    OFFICER = 3
    OWNER = 4

    ROLE_CHOICES = (
        (BANNED, 'Banned'),
        (APPlICANT, 'Applicant'),
        (MEMBER, 'Member'),
        (OFFICER, 'Officer'),
        (OWNER, 'Owner'),
    )

    role = models.SmallIntegerField(
        blank=False, default=APPlICANT, choices=ROLE_CHOICES)

    def promotion_member_demotion_owner(self):
        self.role = User.OFFICER
        self.save()

    def demotion(self):
        self.role = User.MEMBER
        self.save()

    def change_owner(self, current_owner_id):
        owner = User.objects.get(pk=current_owner_id)
        owner.role = User.OFFICER
        owner.save()
        self.role = User.OWNER
        self.save()

    def is_owner(self):
        return self.role == 4

    def is_member(self):
        return self.role == 2
