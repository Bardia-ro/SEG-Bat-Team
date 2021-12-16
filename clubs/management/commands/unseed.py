from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        m = 0
        for i in range(User.objects.all().count()):
            if not User.objects.all()[m].is_superuser:
                User.objects.all()[m].delete()
            else:
                m = m+1
        Club.objects.all().delete()