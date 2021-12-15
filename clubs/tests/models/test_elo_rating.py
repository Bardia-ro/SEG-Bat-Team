from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Role, Elo_Rating, Match

class EloRating(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_elo_rating.json']

    # def setUp(self):
    #     self.user= User.objects.get(email='johndoe@example.org')
    #     self.club= Club.objects.get(name='Club A')
    #     second_user = User.objects.get('janedoe@example.com')
    #     third_user = User.objects.get('samdoe@example.org')
    #     self.role= Role.objects.get(club=self.club, user__id=self.user.id)
    #     self.match = Match.objects.get()
    #     self.Elo_rating = Elo_Rating.objects.get(club = self.club, match = )