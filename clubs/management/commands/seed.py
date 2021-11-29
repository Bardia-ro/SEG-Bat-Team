from django.core.management.base import BaseCommand, CommandError
from django.db import models
from faker import Faker
from clubs.models import User


class Command(BaseCommand):
    PASSWORD = "Password123"

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        fake = Faker()
        for i in range (100):
            fake_first_name = fake.first_name()
            fake_last_name = fake.last_name()
            fake_email=fake_first_name.lower() + fake_last_name.lower() + "@example.com"
            fake_bio = self.faker.text(max_nb_chars=520)
            fake_personal_satement= self.faker.text(max_nb_chars=520)
            User.objects.create(
                email=fake_email,
                first_name=fake_first_name, 
                last_name=fake_last_name, 
                bio=fake_bio,
                experience= 'Class D',
                personal_statement = fake_personal_satement,
                password = 'Password123')
