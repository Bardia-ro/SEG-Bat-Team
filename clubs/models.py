from django.core.validators import RegexValidator
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BLANK_CHOICE_DASH, proxy
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):

    class UserTypes(models.TextChoices):
        CLUBOWNER = 'CLUBOWNER', _('ClubOwner')
        OFFICER = 'OFFICER', _('Officer')
        MEMBER = 'MEMBER', _('Member')

    type = models.CharField(_("Type"), max_length=50, choices=UserTypes.choices , default=UserTypes.MEMBER)

    #will replace this with email instead of username
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    #email = models.EmailField(unique=True, blank=False)
    email = models.EmailField(_('email'), unique = True)
    bio = models.CharField(max_length=520, blank=True)
    experience = models.CharField(max_length = 520,blank = False)
    personal_statement = models.CharField(max_length=600,blank=False)


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
    objects = OwnerCase()
    class Meta:
        proxy =True
