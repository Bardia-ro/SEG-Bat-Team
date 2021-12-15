"""Tests for the edit_profile view"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.forms import EditProfileForm

class EditProfileViewTestCase(TestCase):
    """Tests for the edit_profile view"""

    fixtures = [
        "clubs/tests/fixtures/default_user.json", 
        "clubs/tests/fixtures/other_users.json", 
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json"
    ]

    def setUp(self):
        self.url = reverse('edit_profile', kwargs={"club_id": 0, "user_id": 200})

    def test_edit_profile_url(self):
        self.assertEqual(self.url, '/edit_profile/0/200/')

    def test_non_logged_in_user_gets_edit_profile_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/edit_profile/0/200/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_user_gets_own_edit_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIsInstance(response.context['form'], EditProfileForm)   
        self.assertEqual(response.context['club_id'], 0)
        self.assertTrue(response.context['request_user_is_member'])
        user = User.objects.get(id=200)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())
        self.assertContains(response, 'Save')

    def test_redirect_user_get_another_user_edit_profile_page_from_different_club(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        url = reverse('edit_profile', kwargs={"club_id": 1,"user_id": 10})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        user = User.objects.get(id=200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0)
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])
        
    def test_redirect_user_gets_other_user_edit_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        url = reverse('edit_profile', kwargs={"club_id": 0,"user_id": 2})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        user = User.objects.get(id=200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0) 
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])


    def test_user_makes_valid_post_request_to_own_edit_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(user.experience, 'class D')
        form_data = {
            'first_name': 'John', 
            'last_name': 'Doe', 
            'bio': 'Hey guys!', 
            'experience': 'class A', 
            'personal_statement': 'Hi everyone. I love chess!'
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
        self.assertEqual(user.experience, 'class A')

    def test_user_makes_post_request_with_invalid_data_to_own_edit_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        form_data = {'first_name': '', 
            'last_name': 'Doe', 
            'bio': 'Hi, I am John and I am eighteen years old', 
            'experience': 'class A', 
            'personal_statement': 'I love chess'}
        response = self.client.post(self.url, form_data)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIsInstance(response.context['form'], EditProfileForm)
        self.assertEqual(response.context['club_id'], 0)  
        self.assertTrue(response.context['request_user_is_member'])
        user = User.objects.get(id=200)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())
        self.assertContains(response, 'Save')
        first_name_form_field_error_messages = response.context['form'].fields['first_name'].error_messages
        self.assertTrue('required' in first_name_form_field_error_messages)

    def test_non_logged_in_user_gets_profile(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/edit_profile/0/200/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')