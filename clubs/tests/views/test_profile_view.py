"""Tests for the view which diplays a user's profile"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class ProfileViewTestCase(TestCase):
    """Tests for the view which diplays a user's profile"""

    fixtures = [
        "clubs/tests/fixtures/default_user.json", 
        "clubs/tests/fixtures/specific_users.json", 
        "clubs/tests/fixtures/specific_roles.json", 
        "clubs/tests/fixtures/specific_clubs.json"
    ]

    def setUp(self):
        self.url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/0/200')

    def test_non_logged_in_user_gets_user_profile_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/profile/0/200'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_user_not_associated_with_a_club_gets_own_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertFalse(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Edit profile')

    def test_applicant_user_gets_own_profile_page(self):
        self.client.login(email="adamkirby@example.org", password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 35})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='adamkirby@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertFalse(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Edit profile')
        
    def test_member_user_gets_own_profile_page(self):
        user = User.objects.get(id=76)
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 76})
        self.client.login(email='randygarcia@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Edit profile')

    def test_non_applicant_user_gets_other_user_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1, "user_id": 76})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])

    def test_applicant_user_gets_other_user_profile_page(self):
        self.client.login(email="adamkirby@example.org", password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 76})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 35})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='adamkirby@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])  

    def test_member_user_gets_applicant_user_profile_page(self):
        self.client.login(email='randygarcia@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 35})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 76})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='randygarcia@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])

    def test_member_user_gets_other_member_profile_page(self):
        self.client.login(email='randygarcia@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 101})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 76})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='randygarcia@example.org')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])

    def test_officer_gets_applicant_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 35})
        self.client.login(email='erinswanson@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=35)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Approve membership')

    def test_officer_gets_member_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 76})
        self.client.login(email='erinswanson@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=76)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)

    def test_officer_gets_officer_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 102})
        self.client.login(email='erinswanson@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=102)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)

    def test_officer_gets_owner_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 103})
        self.client.login(email='erinswanson@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=103)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
    
    def test_owner_gets_applicant_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 35})
        self.client.login(email='billie@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=35)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Approve membership')

    def test_owner_gets_member_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 76})
        self.client.login(email='billie@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=76)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Promote to officer')

    def test_owner_gets_officer_profile_page(self):
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 102})
        self.client.login(email='billie@example.org', password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=102)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])  
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Demote to member')
        self.assertContains(response, 'Transfer ownership')

    def _assert_response_contains_content(self, response, user):
            self.assertContains(response, user.first_name)
            self.assertContains(response, user.last_name)
            self.assertContains(response, user.email)
            self.assertContains(response, user.bio)
            self.assertContains(response, user.experience)
            self.assertContains(response, user.personal_statement)    