# Generated by Django 3.2.8 on 2021-11-30 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20211129_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=600)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.SmallIntegerField(choices=[(0, 'Banned'), (1, 'Applicant'), (2, 'Member'), (3, 'Officer'), (4, 'Owner')], default=1)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='users',
            field=models.ManyToManyField(through='clubs.Role', to=settings.AUTH_USER_MODEL),
        ),
    ]