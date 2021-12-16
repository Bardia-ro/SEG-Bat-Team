from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, UserInClub

class ClubTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                "clubs/tests/fixtures/other_users.json",
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.club=Club.objects.get(name='Club A')
        self.role=UserInClub.objects.get(club=self.club, user__id=self.user.id)

    def test_valid_club(self):
        self.assert_club_is_valid()

    def test_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid()
    
    def test_name_must_not_be_over_50_characters(self):
        self.club.name = 'x' *51
        self.assert_club_is_invalid()
    
    def test_name_accepts_50_characters(self):
        self.club.name = 'x' *50
        self.assert_club_is_valid()
    
    def test_name_must_be_unique(self):
        self.club.name = 'Club B'
        self.assert_club_is_invalid()

    def test_description_must_not_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid()

    def test_description_accepts_600_characters(self):
        self.club.description = 'x'*600
        self.assert_club_is_valid()
    
    def test_description_must_not_be_over_600_characters(self):
        self.club.description = 'x'*601
        self.assert_club_is_invalid()
    
    def test_city_accepts_255_characters(self):
        self.club.city = 'x'*255
        self.assert_club_is_valid()
    
    def test_city_must_not_be_over_255_characters(self):
        self.club.city = 'x'*256
        self.assert_club_is_invalid()

    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Club should be valid')

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()