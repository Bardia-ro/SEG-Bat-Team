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
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json']

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

    def test_request_toggle_when_owner_rejects(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        user =User.objects.get(id=200)
        self.assertEqual(user.get_role_as_text_at_club(0), "Owner")
        url = reverse('request_toggle', kwargs={"user_id": 200, "club_id": 0})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.get_role_as_text_at_club(0), "Owner")
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
    
    def test_request_toggle_to_leave_club(self):
        a_member=User.objects.get(pk=2)
        self.assertEqual(a_member.get_role_as_text_at_club(0), "Member")
        self.client.login(email=a_member.email, password='Password123')
        url = reverse('request_toggle', kwargs={"user_id": 2, "club_id": 0})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_member.get_role_as_text_at_club(0), "Not a member")

    def test_request_toggle_to_enter_club(self):
        non_member=User.objects.get(pk=200)
        self.assertEqual(non_member.get_role_as_text_at_club(1), "Not a member")
        self.client.login(email=non_member.email, password='Password123')
        url = reverse('request_toggle', kwargs={"user_id": 200, "club_id": 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(non_member.get_role_as_text_at_club(1), "Application Pending")