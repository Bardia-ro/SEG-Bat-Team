from django.core.management.base import BaseCommand, CommandError
from clubs.models import *

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        User.objects.exclude(email="admin@example.org").delete()
        Club.objects.all().delete()
        UserInClub.objects.all().delete()
        Tournament.objects.all().delete()
        Match.objects.all().delete()
        EliminationMatch.objects.all().delete()
        Elo_Rating.objects.all().delete()
        Group.objects.all().delete()
        GroupMatch.objects.all().delete()
        GroupMatchNextMatches.objects.all().delete()
        GroupPoints.objects.all().delete()


