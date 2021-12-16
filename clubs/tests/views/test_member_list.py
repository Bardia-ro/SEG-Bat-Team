from django.test import TestCase
from django.urls import reverse
from clubs.models import User, UserInClub
from clubs.tests.helpers import reverse_with_next

class MemberListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.url = reverse('member_list', kwargs={'club_id': 0})
        self.user = User.objects.get(email='johndoe@example.org')
        self.members = UserInClub.objects.filter(club__id=0, role=2)
        self.owner = UserInClub.objects.filter(club__id=0, role=4)
        self.officers = UserInClub.objects.filter(club__id=0, role=3)

    def test_member_list_url(self):
        self.assertEqual(self.url,'/member_list/0/')

    def test_get_member_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_list.html')
        for member in self.members.union(self.owner,self.officers):
            user=member.user
            self.assertContains(response, user.first_name)
            self.assertContains(response, user.last_name)
            self.assertContains(response, user.bio)
            user_url = reverse('profile', kwargs={'club_id': 0 ,'user_id': user.id})
            self.assertContains(response, user_url)

    def test_redirect_member_list_if_not_member_of_club(self):
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('member_list', kwargs={"club_id": 9})
        self.assertNotEqual(self.user.get_role_as_text_at_club(9), "Officer")
        self.assertNotEqual(self.user.get_role_as_text_at_club(9), "Owner")
        self.assertNotEqual(self.user.get_role_as_text_at_club(9), "Member")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], user)
        
    
    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
