# Generated by Django 3.2.8 on 2021-12-17 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20211217_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elo_rating',
            name='rating',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='elo_rating',
            name='rating_before',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='userinclub',
            name='elo_rating',
            field=models.IntegerField(default=1000),
        ),
    ]
