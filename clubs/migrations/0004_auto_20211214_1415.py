# Generated by Django 3.2.8 on 2021-12-14 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_auto_20211214_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmatch',
            name='display',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='groupmatch',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='clubs.group'),
        ),
    ]