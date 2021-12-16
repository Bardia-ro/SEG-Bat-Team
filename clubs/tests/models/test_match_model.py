from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Tournament, Match

class MatchModelTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_tournament.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.tournament=Tournament.objects.get(name='Tournament 1')
        self.match=Match.objects.get(id=1)
    
    def test_valid_match_model(self):
        self.assert_match_is_valid()

    def test_match_model_number_cannot_be_blank(self):
        self.match.number=None
        self.assert_match_is_invalid()

    def test_match_player1_cannot_be_blank(self):
        self.match.player1=None
        self.assert_match_is_invalid()

    def test_match_player2_cannot_be_blank(self):
        self.match.player2=None
        self.assert_match_is_invalid()
    
    # def test_player1_and_player2_are_in_same_tournament(self):
    #     self.match.player1=self.user
    #     self.assert_match_is_invalid()

    def assert_match_is_valid(self):
        try:
            self.match.full_clean()
        except (ValidationError):
            self.fail('Match should be valid')

    def assert_match_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.match.full_clean()