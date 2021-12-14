# Generated by Django 3.2.8 on 2021-12-14 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('bio', models.CharField(blank=True, max_length=520)),
                ('experience', models.CharField(max_length=520)),
                ('personal_statement', models.CharField(max_length=600)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('city', models.CharField(max_length=255)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('description', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=600)),
                ('capacity', models.SmallIntegerField(choices=[(2, 'Two'), (4, 'Four'), (8, 'Eight'), (16, 'Sixteen'), (32, 'Thirty_Two'), (64, 'Sixty_Four')])),
                ('deadline', models.DateTimeField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('players', models.ManyToManyField(related_name='_clubs_tournament_players_+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo_rating', models.IntegerField(default=1000)),
                ('role', models.SmallIntegerField(choices=[(0, 'No_club'), (1, 'Applicant'), (2, 'Member'), (3, 'Officer'), (4, 'Owner')], default=1)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('player1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Elo_Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1000)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.match')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EliminationMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.match')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.tournament')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('winner_next_match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='clubs.match')),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='users',
            field=models.ManyToManyField(through='clubs.Role', to=settings.AUTH_USER_MODEL),
        ),
    ]
