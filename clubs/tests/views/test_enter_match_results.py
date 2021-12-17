"""Tests of the match schedule option."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.helpers import tournament_organiser_only
from clubs.models import Tournament, User, Club,EliminationMatch,Match
from clubs.tests.helpers import LogInTester, reverse_with_next

class EnterMatchResultsTestCase(TestCase, LogInTester):
    """Tests of the match schedule view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.url = reverse('enter_match_results', kwargs={'club_id': 0, 'tournament_id': 1,'match_id':1})
        self.user = User.objects.get(pk=5)

    def test_match_result_url(self):
        self.assertEqual(self.url,'/enter_match_results/0/1/1/')

    def test_non_logged_in_user_gets_match_schedule_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/enter_match_results/0/1/1/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    #def test_get_match_schedule(self):
        #self.client.login(email='tomdoe@example.org', password='Password123')
        #elimination_match = EliminationMatch.objects.get(pk=1)
        #self.assertEqual(elimination_match.winner,None)
        #response = self.client.get(self.url)

        #self.assertEqual(response.status_code, 200)
        #elimination_match
        #self.assertEqual(elimination_match.winner)
