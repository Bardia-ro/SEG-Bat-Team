from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Role, Tournament

class TournamentTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                "clubs/tests/fixtures/other_users.json",
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.club=Club.objects.get(name='Club A')
        self.role=Role.objects.get(club=self.club, user__id=self.user.id)
        self.tournament=Tournament.objects.get(name='Tournament 1')

    def test_valid_club(self):
        self.assert_tournament_is_valid()

    def test_name_must_not_be_blank(self):
        self.tournament.name = ''
        self.assert_tournament_is_invalid()
    
    def test_name_must_be_unique(self):
        self.tournament.name='Tournament 2'
        self.assert_tournament_is_invalid()

    def test_name_accepts_50_characters(self):
        self.tournament.name = 'x'*50
        self.assert_tournament_is_valid()

    def test_name_must_not_be_over_50_characters(self):
        self.tournament.name = 'x'*51
        self.assert_tournament_is_invalid()

    def test_capacity_accepts_choice(self):
        self.tournament.capacity = 32
        self.assert_tournament_is_valid()

    def test_capacity_rejects_unknown_choice(self):
        self.tournament.capacity = 100
        self.assert_tournament_is_invalid()

    def test_capacity_is_not_blank_(self):
        self.tournament.capacity = ''
        self.assert_tournament_is_invalid()

    def test_deadline_is_formatted_correctly(self):
        self.tournament.deadline = "1999-03-0420:50"
        self.assert_tournament_is_invalid()
    
    def test_deadline_cannot_be_blank(self):
        self.tournament.deadline = ''
        self.assert_tournament_is_invalid()

    def test_tournament_takes_valid_club(self):
        self.tournament.club=None
        self.assert_tournament_is_invalid()

    def test_tournament_only_takes_officer_as_organiser(self):
        self.tournament.organiser=User.objects.get(id=2)
        self.assert_tournament_is_invalid()

    def test_number_of_players_is_less_than_capacity(self):
        self.tournament.players.add(200)
        self.assert_tournament_is_invalid()

    def test_current_stage_is_one_of_choices(self):
        self.tournament.current_stage='XYZ'
        self.assert_tournament_is_invalid()
    
    def assert_tournament_is_valid(self):
        try:
            self.tournament.full_clean()
        except (ValidationError):
            self.fail('Tournament should be valid')

    def assert_tournament_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tournament.full_clean()