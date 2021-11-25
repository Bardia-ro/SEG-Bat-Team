"""Tests for the view which diplays a user's profile"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class ProfileViewTestCase(TestCase):
    """Tests for the view which diplays a user's profile"""

    fixtures = ["clubs/tests/fixtures/default_user.json", "clubs/tests/fixtures/other_users.json"]

    def setUp(self):
        self.url = reverse('profile', kwargs={"user_id": 0})

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/0')

    def test_non_logged_in_user_gets_user_profile_page(self):
        pass

    def test_applicant_user_gets_own_profile_page(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')   
        
    def test_member_user_gets_own_profile_page(self):
        other_user = User.objects.get(id=1)
        url = reverse('profile', kwargs={"user_id": 1})
        response = self.client.get(url, user_id=1)

    def test_applicant_user_gets_other_user_profile_page(self):
        pass

    def test_member_user_gets_applicant_user_profile_page(self):
        pass

    def test_member_user_gets_other_member_profile_page(self):
        pass