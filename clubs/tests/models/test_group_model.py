from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Tournament, Match, Group

class GroupModelTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.tournament=Tournament.objects.get(name='Tournament 1')
        self.match=Match.objects.get(id=1)
        self.group=Group.objects.get(id=1)
    
    def test_valid_match_model(self):
        self.assert_group_model_is_valid()
    
    def test_number_cannot_be_blank(self):
        self.group.number=''
        self.assert_group_model_is_invalid()

    def test_tournaments_cannot_be_blank(self):
        self.group.tournament=None
        self.assert_group_model_is_invalid()

    def assert_group_model_is_valid(self):
        try:
            self.group.full_clean()
        except (ValidationError):
            self.fail('Elo_rating should be valid')

    def assert_group_model_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.group.full_clean()