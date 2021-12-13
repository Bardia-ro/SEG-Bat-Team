"""Tests of the club page view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class ClubPageTestCase(TestCase, LogInTester):
    """Tests of the log in view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',]

    def setUp(self):
        self.url = reverse('club_page', kwargs={"club_id": 0})
        self.user = User.objects.get(email='johndoe@example.org')

    def test_club_page_url(self):
        self.assertEqual(self.url,'/club_page/0/')

    def test_non_logged_in_user_gets_club_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/club_page/0/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')
    
    def test_user_opens_correct_club_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_page.html')
        self.assertEqual(response.context['club_id'], 0)