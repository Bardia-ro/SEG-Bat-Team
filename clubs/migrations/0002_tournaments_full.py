# Generated by Django 3.2.8 on 2021-12-11 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournaments',
            name='full',
            field=models.BooleanField(default=False),
        ),
    ]