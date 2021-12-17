from contextlib import nullcontext
from django.core.exceptions import ValidationError
from django.forms.fields import NullBooleanField
from django.test import TestCase
from clubs.models import Club, User, UserInClub, Elo_Rating, Match

class EloRating(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_tournament.json',
                'clubs/tests/fixtures/default_elo_ratings.json']

    def setUp(self):
        self.user= User.objects.get(email='johndoe@example.org')
        self.elo_rating = Elo_Rating.objects.get(id=1)

    def test_valid_elo_rating(self):
        self.assert_elo_rating_is_valid()

    def test_result_can_be_null(self):
        self.elo_rating.result__isnull=True
        self.assert_elo_rating_is_valid()

    def test_rating_cannot_be_blank(self):
        self.elo_rating.rating=None
        self.assert_elo_rating_is_invalid()

    def test_user_cannot_be_blank(self):
        self.elo_rating.user=None
        self.assert_elo_rating_is_invalid()

    def test_club_cannot_be_blank(self):
        self.elo_rating.club=None
        self.assert_elo_rating_is_invalid()

    def test_match_cannot_be_blank(self):
        self.elo_rating.match=None
        self.assert_elo_rating_is_invalid()

    def assert_elo_rating_is_valid(self):
        try:
            self.elo_rating.full_clean()
        except (ValidationError):
            self.fail('Elo_rating should be valid')

    def assert_elo_rating_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.elo_rating.full_clean()
