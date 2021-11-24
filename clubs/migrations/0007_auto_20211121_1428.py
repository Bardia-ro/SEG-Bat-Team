# Generated by Django 3.2.9 on 2021-11-21 14:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_alter_user_personal_statement'),
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