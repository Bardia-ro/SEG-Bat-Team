from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.lookups import Regex
#from django.db.models.fields import BLANK_CHOICE_DASH, proxy


# Create your models here.
class User(AbstractUser):
    bio = models.TextField()
    # UserTypes = (
    # ('OFFICER', 'Officer'),
    # ('CLUBOWNER', 'ClubOwner'),
    # ('MEMBER', 'Member')
    # )

    # type = models.CharField(max_length=50, choices=UserTypes, default='MEMBER') 

    # username = models.CharField(
    #     blank=False,
    #     max_length=30,
    #     unique = True,
    #     validators=[RegexValidator(
    #         regex=r'^@\w{3,}$',
    #         message='username must consist of @ followed by at least 3 alphanumerical'
    #     )]

    # )
    # first_name = models.CharField(max_length=50, blank=False)
    # last_name = models.CharField(max_length=50, blank=False)
    # email = models.EmailField(unique=True, blank=False)
    # bio = models.CharField(max_length=520, blank=True)
    # experience = models.CharField(max_length = 520, blank = False)
    # personal_statement = models.CharField(max_length=600, blank=False)


