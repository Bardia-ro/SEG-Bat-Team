"""Tests for the view which diplays a user's profile"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User


class ProfileViewTestCase(TestCase):
    """Tests for the view which diplays a user's profile"""

    fixtures = [ "clubs/tests/fixtures/default_user.json", 
        "clubs/tests/fixtures/other_users.json", 
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json"]

    def setUp(self):
        self.url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/0/200/')

    def test_non_logged_in_user_gets_user_profile_page(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/profile/0/200/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_gets_own_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0) 
        self.assertFalse(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Edit profile')

    def test_redirect_applicant_getting_other_profile_page(self):
        self.client.login(email="jamiescott@example.org", password='Password123')
        url = reverse('profile', kwargs={"club_id": 0,"user_id": 200})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 6})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='jamiescott@example.org')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 0)  
        self.assertTrue(response.context['is_current_user'])
        self.assertContains(response, 'Edit profile')
        
    def test_redirect_member_getting_other_profile_page(self):
        self.client.login(email='janedoe@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 0,"user_id": 200})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 2})
        self.assertRedirects(response, expected_url)
        user = User.objects.get(id=2)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)  
        self.assertEqual(response.context['club_id'], 0)  
        self.assertTrue(response.context['is_current_user'])
        self.assertContains(response, 'Edit profile')

    def test_redirect_non_applicant_or_member_of_club_user_gets_other_user_profile_page(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1, "user_id": 9})
        response = self.client.get(url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 0, "user_id": 200})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='johndoe@example.org')
        self.assertEqual(response.context['user'], user)  
        self.assertEqual(response.context['club_id'], 0) 
        self.assertFalse(response.context['request_user_is_member'])
        self.assertTrue(response.context['is_current_user'])
        self.assertContains(response, 'Edit profile')

    def test_redirect_officer_getting_user_not_associated_with_club_profile_page(self):
        self.client.login(email='richardfernandez@example.org', password='Password123')
        response = self.client.get(self.url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 11})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(id=11)
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)  
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 3)
        self.assertEqual(response.context['user_role'], 3)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())

    def test_officer_gets_applicant_profile_page(self):
        self.client.login(email='richardfernandez@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 13})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=13)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1) 
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 3)
        self.assertEqual(response.context['user_role'], 1)
        request_user = User.objects.get(id=11)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Approve membership')        

    def test_officer_gets_member_profile_page(self):
        self.client.login(email='richardfernandez@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 10})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=10)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)    
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 3)
        self.assertEqual(response.context['user_role'], 2)
        request_user = User.objects.get(id=11)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
        self._assert_response_contains_content(response, user)

    def test_officer_gets_other_officer_profile_page(self):
        self.client.login(email='richardfernandez@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 12})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=12)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)    
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 3)
        self.assertEqual(response.context['user_role'], 3)
        request_user = User.objects.get(id=11)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member()) 
        self._assert_response_contains_content(response, user)

    def test_officer_gets_owner_profile_page(self):
        self.client.login(email='richardfernandez@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1,"user_id": 8})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=8)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)   
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 3)
        self.assertEqual(response.context['user_role'], 4)
        request_user = User.objects.get(id=11)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
        self._assert_response_contains_content(response, user)
    
    def test_redirect_owner_gets_user_not_associated_with_club_profile_page(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        response = self.client.get(self.url, follow=True)
        expected_url = reverse('profile', kwargs={"club_id": 1, "user_id": 8})
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(email='jessekim@example.org')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)  
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertTrue(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 4)
        self.assertEqual(response.context['user_role'], 4)
        self.assertQuerysetEqual(response.context['club_list'], user.get_clubs_user_is_a_member())
    
    def test_owner_gets_applicant_profile_page(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1, "user_id": 13})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=13)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)    
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 4)
        self.assertEqual(response.context['user_role'], 1)
        request_user = User.objects.get(id=8)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Approve membership')

    def test_owner_gets_member_profile_page(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1, "user_id": 10})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=10)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)    
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 4)
        self.assertEqual(response.context['user_role'], 2)
        request_user = User.objects.get(id=8)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
        self._assert_response_contains_content(response, user)
        self.assertContains(response, 'Promote to officer')

    def test_owner_gets_officer_profile_page(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        url = reverse('profile', kwargs={"club_id": 1, "user_id": 12})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=12)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['club_id'], 1)    
        self.assertTrue(response.context['request_user_is_member']) 
        self.assertFalse(response.context['is_current_user'])
        self.assertEqual(response.context['request_user_role'], 4)
        self.assertEqual(response.context['user_role'], 3)
        request_user = User.objects.get(id=8)
        self.assertQuerysetEqual(response.context['club_list'], request_user.get_clubs_user_is_a_member())
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

    def test_owner_promotes_member_to_officer(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        user = User.objects.get(id=10)
        new_url = reverse('promote_member_to_officer', kwargs={"club_id": 1, "member_id": 10})
        response=self.client.get(new_url, follow=True)
        self.assertEqual(response.status_code, 200)
        role=user.get_role_as_text_at_club(1)
        self.assertEqual(role, "Officer")

    def test_demote_officer_to_member(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        user = User.objects.get(id=12)
        new_url = reverse('demote_officer_to_member', kwargs={"club_id": 1, "officer_id": 12})
        response=self.client.get(new_url, follow=True)
        self.assertEqual(response.status_code, 200)
        role=user.get_role_as_text_at_club(1)
        self.assertEqual(role, "Member")

    def test_transfer_ownership(self):
        self.client.login(email='jessekim@example.org', password='Password123')
        owner = User.objects.get(id=8)
        user = User.objects.get(id=12)
        new_url = reverse('transfer_ownership', kwargs={"club_id": 1, "new_owner_id": 12})
        response=self.client.get(new_url, follow=True)
        self.assertEqual(response.status_code, 200)
        role=user.get_role_as_text_at_club(1)
        old_owner_role= owner.get_role_as_text_at_club(1)
        self.assertEqual(role, "Owner")
        self.assertEqual(old_owner_role, "Officer")
        