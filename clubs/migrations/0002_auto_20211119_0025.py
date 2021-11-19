# Generated by Django 3.2.9 on 2021-11-19 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubOwner',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clubs.user',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clubs.user',),
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clubs.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('OFFICER', 'Officer'), ('CLUBOWNER', 'ClubOwner'), ('MEMBER', 'Member')], default='MEMBER', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]