# Generated by Django 3.2.5 on 2021-11-22 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0007_auto_20211122_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]