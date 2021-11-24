from django.core.validators import RegexValidator
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BLANK_CHOICE_DASH, proxy
from django.utils.translation import gettext_lazy as _
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe


class User(AbstractUser):

    class UserTypes(models.TextChoices):
        CLUBOWNER = 'CLUBOWNER', _('ClubOwner')
        OFFICER = 'OFFICER', _('Officer')
        MEMBER = 'MEMBER', _('Member')
        APPLICANT = 'APPLICANT', _('Applicant')

    type = models.CharField(_("Type"), max_length=50, choices=UserTypes.choices , default=UserTypes.APPLICANT)

    #will replace this with email instead of username
    username = models.CharField(max_length=50, unique = True)

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    #email = models.EmailField(unique=True, blank=False)
    email = models.EmailField(_('email'), unique = True)
    bio = models.CharField(max_length=520, blank=True)
    experience = models.CharField(max_length = 520,blank = False)
    personal_statement = models.CharField(max_length=600,blank=False)

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


class ApplicantCase(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type = User.UserTypes.APPLICANT)

class MemberCase(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type = User.UserTypes.MEMBER)

class OfficerCase(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type = User.UserTypes.OFFICER)

class OwnerCase(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type =  User.UserTypes.CLUBOWNER)

class Officer(User):
    objects = OfficerCase()
    class Meta:
            proxy = True

class ClubOwner(User):
    objects = OwnerCase()
    class Meta:
        proxy =True

class Member(User):
    objects = MemberCase()
    class Meta:
        proxy =True

class Applicant(User):
    objects = ApplicantCase()
    class Meta:
        proxy =True
