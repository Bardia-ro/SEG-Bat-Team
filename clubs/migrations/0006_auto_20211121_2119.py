# Generated by Django 3.2.5 on 2021-11-21 21:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.CharField(max_length=520),
        ),
        migrations.AlterField(
            model_name='user',
            name='personal_statement',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username must consist of @ followed by at least three alphanumericals', regex='^@\\w{3,}$')]),
        ),
    ]
