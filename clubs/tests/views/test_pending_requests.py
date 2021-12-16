"""Tests for the view which diplays the pending request page"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User,Club,UserInClub


class ProfileViewTestCase(TestCase):
    """Tests for the view which diplays the applicats pending request page"""

    fixtures = [ "clubs/tests/fixtures/default_user.json", 
        "clubs/tests/fixtures/other_users.json", 
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json"]

    def setUp(self):
        self.user=User.objects.get(email='christinacastro@example.org')
        self.club=Club.objects.get(id=1)
        self.applicants=UserInClub.objects.filter(club=self.club,role=1)
        self.url = reverse('pending_requests', kwargs={"club_id": 1})

    def test_pending_request_url(self):
        self.assertEqual(self.url, '/pending_requests/1/')

    def test_non_logged_in_user_gets_pending_requests_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/pending_requests/1/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_get_pending_request(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_requests.html')
        for member in self.applicants:
            user=User.objects.get(id=member.user_id)
            self.assertContains(response, user.email)
            user_url = reverse('profile', kwargs={'club_id': 1 ,'user_id': user.id})
            self.assertContains(response, user_url)

    def test_redirect_if_not_officer_of_owner_of_club(self):
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('pending_requests', kwargs={"club_id": 9})
        self.assertNotEqual(self.user.get_role_as_text_at_club(9), "Officer")
        self.assertNotEqual(self.user.get_role_as_text_at_club(9), "Owner")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=8)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
    
    def test_approve_member(self):
        self.client.login(email=self.user.email, password='Password123')
        user =User.objects.get(id=14)
        self.assertEqual(user.get_role_as_text_at_club(1), "Application Pending")
        url = reverse('approve_member', kwargs={"club_id": 1, "applicant_id": 14})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.get_role_as_text_at_club(1), "Member")

    def test_reject_member(self):
        self.client.login(email=self.user.email, password='Password123')
        user =User.objects.get(id=14)
        self.assertEqual(user.get_role_as_text_at_club(1), "Application Pending")
        url = reverse('reject_member', kwargs={"club_id": 1, "applicant_id": 14})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.get_role_as_text_at_club(1), "Not a member")
 