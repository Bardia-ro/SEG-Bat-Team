# Generated by Django 3.2.8 on 2021-12-03 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_auto_20211203_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]
