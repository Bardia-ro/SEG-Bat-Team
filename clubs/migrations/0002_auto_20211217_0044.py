# Generated by Django 3.2.8 on 2021-12-17 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elo_rating',
            name='rating',
            field=models.FloatField(default=1000),
        ),
        migrations.AlterField(
            model_name='elo_rating',
            name='rating_before',
            field=models.FloatField(default=1000),
        ),
        migrations.AlterField(
            model_name='userinclub',
            name='elo_rating',
            field=models.FloatField(default=1000),
        ),
    ]
