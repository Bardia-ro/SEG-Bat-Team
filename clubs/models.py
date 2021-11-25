from django.core.validators import RegexValidator
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import BLANK_CHOICE_DASH, proxy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    class UserTypes(models.TextChoices):
        CLUBOWNER = 'CLUBOWNER', _('ClubOwner')
        OFFICER = 'OFFICER', _('Officer')
        MEMBER = 'MEMBER', _('Member')
        APPLICANT = 'APPLICANT', _('Applicant')

    type = models.CharField(_("Type"), max_length=50, choices=UserTypes.choices , default=UserTypes.APPLICANT)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    experience = models.CharField(max_length = 520,blank = False)
    personal_statement = models.CharField(max_length=600,blank=False)

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
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

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
