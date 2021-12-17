"""Tests of the club list navbar option."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.helpers import tournament_organiser_only
from clubs.models import Tournament, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class ClubListTestCase(TestCase, LogInTester):
    """Tests of the club list view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.url = reverse('club_list/0')
        self.user = User.objects.get(email='johndoe@example.org')

    # def test_club_page_url(self):
    #     self.assertEqual(self.url,'/club_page/0/')

    # def test_non_logged_in_user_gets_club_page(self):
    #     response = self.client.get(self.url, follow=True)
    #     expected_url = '/log_in/?next=/club_page/0/'
    #     self.assertRedirects(response, expected_url)
    #     self.assertTemplateUsed(response, 'log_in.html')