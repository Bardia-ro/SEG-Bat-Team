from django.core.management.base import BaseCommand, CommandError
from clubs.models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        User.objects.exclude(email="admin@clucker.com").delete()