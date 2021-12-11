from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Role

class ClubTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.club=Club.objects.get(name='Club A')
        self.role=Role.objects.get(club=self.club)

    def test_valid_club(self):
        self.assert_club_is_valid()

    def test_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid()

    def test_description_must_not_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid()
    
    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Club should be valid')

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()