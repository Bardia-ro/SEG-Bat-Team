"""Tests for the view which diplays a user's profile"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

# class ProfileViewTestCase(TestCase):
#     """Tests for the view which diplays a user's profile"""

#     fixtures = ["clubs/tests/fixtures/default_user.json", "clubs/tests/fixtures/other_users.json"]

#     def setUp(self):
#         self.url = reverse('profile', kwargs={"user_id": 0})

#     def test_profile_url(self):
#         self.assertEqual(self.url, '/profile/0')

#     def test_non_logged_in_user_gets_user_profile_page(self):
#         response = self.client.get(self.url, follow=True)
#         expected_url = '/log_in/?next=/profile/0'
#         self.assertRedirects(response, expected_url)
#         self.assertTemplateUsed(response, 'log_in.html')

#     def test_applicant_user_gets_own_profile_page(self):
#         self.client.login(email='johndoe@example.org', password='Password123')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'profile.html')
#         user = User.objects.get(email='johndoe@example.org')
#         self.assertEqual(response.context['user'], user)   
#         self.assertFalse(response.context['user_is_member']) 
#         self.assertTrue(response.context['is_current_user'])  
#         self.assertContains(response, user.first_name)
#         self.assertContains(response, user.last_name)
#         self.assertContains(response, user.type)
#         self.assertContains(response, user.email)
#         self.assertContains(response, user.bio)
#         self.assertContains(response, user.experience)
#         self.assertContains(response, user.personal_statement)
#         self.assertContains(response, 'Edit profile')
        
#     def test_member_user_gets_own_profile_page(self):
#         user = User.objects.get(id=1)
#         url = reverse('profile', kwargs={"user_id": 1})
#         self.client.login(email='janedoe@example.org', password='Password123')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'profile.html')
#         self.assertEqual(response.context['user'], user)   
#         self.assertTrue(response.context['user_is_member']) 
#         self.assertTrue(response.context['is_current_user'])  
#         self.assertContains(response, user.first_name)
#         self.assertContains(response, user.last_name)
#         self.assertContains(response, user.type)
#         self.assertContains(response, user.email)
#         self.assertContains(response, user.bio)
#         self.assertContains(response, user.experience)
#         self.assertContains(response, user.personal_statement)
#         self.assertContains(response, 'Edit profile')

#     def test_applicant_user_gets_other_user_profile_page(self):
#         self.client.login(email='johndoe@example.org', password='Password123')
#         url = reverse('profile', kwargs={"user_id": 1})
#         response = self.client.get(url, follow=True)
#         expected_url = reverse('profile', kwargs={"user_id": 0})
#         self.assertRedirects(response, expected_url)
#         self.assertTemplateUsed(response, 'profile.html')
#         user = User.objects.get(email='johndoe@example.org')
#         self.assertEqual(response.context['user'], user)   
#         self.assertFalse(response.context['user_is_member']) 
#         self.assertTrue(response.context['is_current_user'])  
#         self.assertContains(response, user.first_name)
#         self.assertContains(response, user.last_name)
#         self.assertContains(response, user.type)
#         self.assertContains(response, user.email)
#         self.assertContains(response, user.bio)
#         self.assertContains(response, user.experience)
#         self.assertContains(response, user.personal_statement)
#         self.assertContains(response, 'Edit profile')

#     def test_member_user_gets_applicant_user_profile_page(self):
#         self.client.login(email='janedoe@example.org', password='Password123')
#         url = reverse('profile', kwargs={"user_id": 0})
#         response = self.client.get(url, follow=True)
#         expected_url = reverse('profile', kwargs={"user_id": 1})
#         self.assertRedirects(response, expected_url)
#         self.assertTemplateUsed(response, 'profile.html')
#         user = User.objects.get(email='janedoe@example.org')
#         self.assertEqual(response.context['user'], user)   
#         self.assertTrue(response.context['user_is_member']) 
#         self.assertTrue(response.context['is_current_user'])  
#         self.assertContains(response, user.first_name)
#         self.assertContains(response, user.last_name)
#         self.assertContains(response, user.type)
#         self.assertContains(response, user.email)
#         self.assertContains(response, user.bio)
#         self.assertContains(response, user.experience)
#         self.assertContains(response, user.personal_statement)
#         self.assertContains(response, 'Edit profile')

#     def test_member_user_gets_other_member_profile_page(self):
#         self.client.login(email='janedoe@example.org', password='Password123')
#         url = reverse('profile', kwargs={"user_id": 2})
#         response = self.client.get(url, follow=True)
#         expected_url = reverse('profile', kwargs={"user_id": 1})
#         self.assertRedirects(response, expected_url)
#         self.assertTemplateUsed(response, 'profile.html')
#         user = User.objects.get(email='janedoe@example.org')
#         self.assertEqual(response.context['user'], user)   
#         self.assertTrue(response.context['user_is_member']) 
#         self.assertTrue(response.context['is_current_user'])  
#         self.assertContains(response, user.first_name)
#         self.assertContains(response, user.last_name)
#         self.assertContains(response, user.type)
#         self.assertContains(response, user.email)
#         self.assertContains(response, user.bio)
#         self.assertContains(response, user.experience)
#         self.assertContains(response, user.personal_statement)
#         self.assertContains(response, 'Edit profile')