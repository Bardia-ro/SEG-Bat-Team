from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Tournament, Match, Group, GroupMatch

class GroupMatchModelTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.tournament=Tournament.objects.get(name='Tournament 2')
        self.match=Match.objects.get(id=1)
        self.group=Group.objects.get(id=1)
        self.group_match=GroupMatch.objects.get(id=1)
    
    def test_valid_match_model(self):
        self.assert_group_match_model_is_valid()

    def test_player1_points_cannot_be_blank(self):
        self.group_match.player1_points=''
        self.assert_group_match_model_is_invalid()

    def test_player2_points_cannot_be_blank(self):
        self.group_match.player2_points=''
        self.assert_group_match_model_is_invalid()

    # def test_player1_gets_point(self):
    #     old_points= self.group_match.player1_points
    #     self.group_match.player1_won_points()
    #     new_points= self.group_match.player1_points
    #     self.assertEqual(old_points+1, new_points)

    def assert_group_match_model_is_valid(self):
        try:
            self.group_match.full_clean()
        except (ValidationError):
            self.fail('Group Match should be valid')

    def assert_group_match_model_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.group_match.full_clean()