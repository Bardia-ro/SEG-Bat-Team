from django.core.management.base import BaseCommand, CommandError
from clubs.models import Tournaments, User, Club

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        User.objects.exclude(email="admin@example.org").delete()
        Club.objects.all().delete()
        Tournaments.objects.all().delete()