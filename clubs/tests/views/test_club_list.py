<<<<<<< HEAD
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import reverse_with_next

class ClubListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json']
=======
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
>>>>>>> 20ed871f57a4ac5344aa801e277206a4c776f81c

    def setUp(self):
        self.url = reverse('club_list', kwargs={'club_id': 0})
        self.user = User.objects.get(email='johndoe@example.org')

<<<<<<< HEAD
    def test_member_list_url(self):
        self.assertEqual(self.url,'/club_list/0/')

    def test_get_member_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        for club in self.clubs:
            club=club
            self.assertContains(response, club.name)
            self.assertContains(response, club.description)
            self.assertContains(response, club.location)
            club_url = reverse('club_page', kwargs={'club_id': club.id})
            self.assertContains(response, club_url)
    
    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
=======
    def test_club_page_url(self):
        self.assertEqual(self.url,'/club_list/0/')

    def test_non_logged_in_user_gets_club_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/club_list/0/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_get_club_list(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        self.assertQuerysetEqual(response.context['clubs'].order_by('name'), Club.objects.all().order_by('name'))
        self.assertEqual(response.context['club_id'], 0)
        self.assertQuerysetEqual(response.context['club_list'], self.user.get_clubs_user_is_a_member())
>>>>>>> 20ed871f57a4ac5344aa801e277206a4c776f81c
