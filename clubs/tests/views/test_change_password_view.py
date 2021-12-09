"""Tests for the change_password view"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.forms import ChangePasswordForm, Password
from django.contrib.auth.hashers import check_password

class ChangePasswordViewTestCase(TestCase):
    """Tests for the change_password view"""

    fixtures = [
        "clubs/tests/fixtures/default_user.json", 
        "clubs/tests/fixtures/specific_users.json", 
        "clubs/tests/fixtures/specific_roles.json", 
        "clubs/tests/fixtures/specific_clubs.json"
    ]

    def setUp(self):
        self.url = reverse('change_password', kwargs={"club_id": 0, "user_id": 200})

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/0/200')

    def test_non_logged_in_user_gets_change_password_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/change_password/0/200'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_user_gets_own_change_password_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        self.assertIsInstance(response.context['form'], ChangePasswordForm)   
        self.assertEqual(response.context['club_id'], 0)
        self.assertFalse(response.context['request_user_is_member'])
        user = User.objects.get(id=200)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())
        self.assertContains(response, 'Change Password')

    def test_user_not_in_club_gets_user_who_is_in_club_change_password_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        url = reverse('change_password', kwargs={"club_id": 1,"user_id": 76})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        user = User.objects.get(id=200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0)
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])
        
    def test_user_gets_other_user_change_password_page(self):
        self.client.login(email='billie@example.org', password='Password123')
        url = reverse('change_password', kwargs={"club_id": 1,"user_id": 76})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 76})
        self.assertRedirects(response, expected_url)
        user = User.objects.get(id=76)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1) 
        self.assertTrue(response.context['request_user_is_member'])
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 4)
        self.assertEqual(response.context['user_role'], 2)
        request_user = User.objects.get(id=103)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())

    def test_user_makes_valid_post_request_to_own_change_password_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        user = User.objects.get(email='johndoe@example.org')
        self.assertTrue(check_password("Password123", user.password))
        form_data = {
            'new_password': 'PassworDNew456', 
            'password_confirmation': 'PassworDNew456', 
        }
        response = self.client.post(self.url, form_data, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0)
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])
        self.assertTrue(check_password("PassworDNew456", user.password))

    def test_user_makes_post_request_with_invalid_data_to_own_change_password_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        form_data = {
            'new_password': 'dfgdfgdfgd10', 
            'password_confirmation': 'dfgdfgdfgd10'
        }
        response = self.client.post(self.url, form_data)
        self.assertTemplateUsed(response, 'change_password.html')
        self.assertIsInstance(response.context['form'], ChangePasswordForm)
        self.assertEqual(response.context['club_id'], 0)  
        self.assertFalse(response.context['request_user_is_member'])
        user = User.objects.get(id=200)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())
        self.assertContains(response, 'Change Password')
        new_password_form_field_error_messages = response.context['form'].fields['new_password'].error_messages
        self.assertTrue('required' in new_password_form_field_error_messages)