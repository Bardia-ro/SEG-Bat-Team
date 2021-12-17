"""Tests of the match schedule option."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.helpers import tournament_organiser_only
from clubs.models import Tournament, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class MatchScheduleTestCase(TestCase, LogInTester):
    """Tests of the match schedule view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.url = reverse('match_schedule', kwargs={'club_id': 0, 'tournament_id': 1})
        self.user = User.objects.get(email='johndoe@example.org')

    def test_club_page_url(self):
        self.assertEqual(self.url,'/match_schedule/0/1/')

    def test_non_logged_in_user_gets_match_schedule_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/match_schedule/0/1/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_get_match_schedule(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'match_schedule.html')
        self.assertEqual(response.context['club_id'], 0)
        self.assertQuerysetEqual(response.context['club_list'], self.user.get_clubs_user_is_a_member())