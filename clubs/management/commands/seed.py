from django.core.management.base import BaseCommand, CommandError
from django.db import models
from faker import Faker
from clubs.models import Tournament, User, Club, Role
import random


class Command(BaseCommand):
    PASSWORD = "Password123"

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        fake = Faker()
        self.create_fake_users(fake)
        self.create_fake_clubs(fake)
        self.create_fake_club_members(fake)


    def create_fake_users(self, fake):
        for i in range (100):
            fake_first_name = fake.first_name()
            fake_last_name = fake.unique.last_name()
            fake_email=fake_first_name.lower() + fake_last_name.lower() + "@example.org"
            fake_bio = fake.paragraph(nb_sentences=5)
            fake_personal_satement= fake.paragraph(nb_sentences=5)
            User.objects.create(
                email=fake_email,
                first_name=fake_first_name, 
                last_name=fake_last_name, 
                bio=fake_bio,
                experience= 'class D',
                personal_statement = fake_personal_satement,
                password = 'pbkdf2_sha256$260000$fHqt6M2oenTaZmOlXyYcwg$e7pf0+y/4iCCWKxF/Dlh4CKGsJXNpYy/FtBEfz0fiuQ=')
        User.objects.create(
                email="jeb@example.org",
                first_name="Jebediah", 
                last_name="Kerman", 
                bio=fake.paragraph(nb_sentences=5),
                experience= 'class D',
                personal_statement = fake.paragraph(nb_sentences=5),
                password = 'pbkdf2_sha256$260000$fHqt6M2oenTaZmOlXyYcwg$e7pf0+y/4iCCWKxF/Dlh4CKGsJXNpYy/FtBEfz0fiuQ=')
        User.objects.create(
                email="val@example.org",
                first_name="Valentina", 
                last_name="Kerman", 
                bio=fake.paragraph(nb_sentences=5),
                experience= 'class D',
                personal_statement = fake.paragraph(nb_sentences=5),
                password = 'pbkdf2_sha256$260000$fHqt6M2oenTaZmOlXyYcwg$e7pf0+y/4iCCWKxF/Dlh4CKGsJXNpYy/FtBEfz0fiuQ=')
        User.objects.create(
                email="billie@example.org",
                first_name="Billie", 
                last_name="Kerman", 
                bio=fake.paragraph(nb_sentences=5),
                experience= 'class D',
                personal_statement = fake.paragraph(nb_sentences=5),
                password = 'pbkdf2_sha256$260000$fHqt6M2oenTaZmOlXyYcwg$e7pf0+y/4iCCWKxF/Dlh4CKGsJXNpYy/FtBEfz0fiuQ=')
        

    def create_fake_clubs(self,fake):
        Club.objects.create(
                name = "Kerbal Chess Club",
                city = "Kerbal",
                description = fake.paragraph(nb_sentences=5)
            )
        for i in range(15):
            fake_name = fake.company()
            fake_city = fake.city()
            fake_description = fake.paragraph(nb_sentences=5)
            Club.objects.create(
                name = fake_name,
                city = fake_city,
                description = fake_description
            )


    def create_fake_club_members(self, fake):
        users = User.objects.all()
        clubs = Club.objects.all()
        counter = 0
        for a_club in clubs:
            if a_club.name =="Kerbal Chess Club":
                Role.objects.create(club=a_club, user=User.objects.get(email="billie@example.org"), role=4)
                Role.objects.create(club=a_club, user=User.objects.get(email="val@example.org"), role=3)
                Role.objects.create(club=a_club, user=User.objects.get(email="jeb@example.org"), role=2)
            else:
                if counter==1:
                    Role.objects.create(club=a_club, user=User.objects.get(email="jeb@example.org"), role=3)
                    Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=4)
                elif counter==2:
                    Role.objects.create(club=a_club, user=User.objects.get(email="val@example.org"), role=4)
                    Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=3)
                else:
                    Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=4)
                    Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=3)

            Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=3)

            if counter ==3:
                Role.objects.create(club=a_club, user=User.objects.get(email="billie@example.org"), role=2)

            for i in range(35):
                Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=2)
            for i in range(3):
                Role.objects.create(club=a_club, user=self.get_random_user(users, a_club), role=1)
            counter=counter+1
            self.create_tournaments(a_club,fake)
            

    def get_random_user(self,users, club):
        found=False
        a_user = ""
        while(found==False):
            a_user=random.choice(users)
            try:
                Role.objects.get(club=club, user=a_user)
            except:
                if(a_user.email[:5]!="admin"):
                    found=True
                    return a_user

    def get_random_capacity(self):
        list= [2,4,8,16,32,64]
        return random.choice(list)

    def get_tournament_players(self,club,organiser):
        found=False
        a_user = ""
        users=Role.objects.filter(club=club)
        while(found==False):
            a_user=random.choice(users)
            if a_user!=organiser:
                return a_user.user

    def create_tournaments(self,a_club, fake):
        if a_club.name !="Kerbal Chess Club":
            the_tournament = Tournament.objects.create(name=f'Tournament {fake.random_int()}',
                description= fake.paragraph(nb_sentences=5),
                capacity=self.get_random_capacity(),
                deadline=fake.future_datetime(),
                club=a_club,
                organiser = Role.objects.filter(club=a_club, role=3).first().user)
            for i in range(0,the_tournament.capacity):
                the_tournament.players.add(self.get_tournament_players(a_club, the_tournament.organiser))
        else:
            the_tournament = Tournament.objects.create(name=f'Tournament {fake.random_int()}',
                description= fake.paragraph(nb_sentences=5),
                capacity=32,
                deadline=fake.future_datetime("+24h"),
                club=Club.objects.get(name="Kerbal Chess Club"),
                organiser = User.objects.get(email="val@example.org"))
            for i in range(0,the_tournament.capacity):
                jeb = User.objects.get(email="jeb@example.org")
                found = False
                while(not found):
                    not_jeb = self.get_tournament_players(a_club, the_tournament.organiser)
                    if (not_jeb!=jeb and not_jeb not in the_tournament.players.all()):
                        found=True
                the_tournament.players.add(not_jeb)
            the_tournament = Tournament.objects.create(name=f'Tournament {fake.random_int()}',
                description= fake.paragraph(nb_sentences=5),
                capacity=16,
                deadline=fake.past_datetime(),
                club=Club.objects.get(name="Kerbal Chess Club"),
                organiser = User.objects.get(email="val@example.org"))
            the_tournament.players.add(User.objects.get(email="jeb@example.org"))
            for i in range(0,the_tournament.capacity-1):
                the_tournament.players.add(self.get_tournament_players(a_club, the_tournament.organiser))