from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Match, Tournament, EliminationMatch

"""
class EliminationMatch(models.Model):

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')
    winner_next_match = models.ForeignKey(Match, null=True, on_delete=models.CASCADE, related_name = '+')

    def set_winner(self, player):
        self.winner = player
        self.save()
        self.set_winner_as_player_in_winner_next_match()

    def set_winner_as_player_in_winner_next_match(self):

        if self.winner_next_match:
            if self.match.number % 2 == 1:
                self.winner_next_match.player1 = self.winner
            else:
                self.winner_next_match.player2 = self.winner

            self.winner_next_match.save()
"""

class EliminationMatchModel(TestCase):

    #fixtures for tournament, match, user, elimination match
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.tournament=Tournament.objects.get(id=0)
        self.match=Match.objects.get(id=0)
        self.winner=User.objects.get(email='johndoe@example.org')
        self.winner_next_match=Match.objects.get(id=1)
        self.elimination_match=EliminationMatch.objects.get(id=0)

    #Testing field attributes
    def test_valid_elimination_match_model(self):
        self.assert_elimination_match_is_valid()

    def test_winner_can_be_null(self):
        self.elimination_match.winner__isnull=True
        self.assert_elimination_match_is_valid()

    def test_winner_next_match_can_be_null(self):
        self.elimination_match.winner_next_match__isnull=True
        self.assert_elimination_match_is_valid()

    def test_tournament_cannot_be_blank(self):
        self.elimination_match.tournament=None
        self.assert_elimination_match_is_invalid()

    def test_match_cannot_be_blank(self):
        self.elimination_match.match=None
        self.assert_elimination_match_is_invalid()

    #Class functionality tests
    #def test_create_elimination_matches(self):
    #    self.tournament._create_elimination_matches()

    #Valid or invalid methods
    def assert_elimination_match_is_valid(self):
        try:
            self.elimination_match.full_clean()
            self.tournament.full_clean()
        except (ValidationError):
            self.fail('Elimination match should be valid')

    def assert_elimination_match_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.elimination_match.full_clean()