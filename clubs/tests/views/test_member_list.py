from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Role
from clubs.tests.helpers import reverse_with_next

class MemberListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.url = reverse('member_list', kwargs={'club_id': 0})
        self.user = User.objects.get(email='johndoe@example.org')
        self.members = Role.objects.filter(club__id=0)

    def test_member_list_url(self):
        self.assertEqual(self.url,'/member_list/0/')

    def test_get_member_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_list.html')
        for member in self.members:
            user=member.user
            self.assertContains(response, user.first_name)
            self.assertContains(response, user.last_name)
            self.assertContains(response, user.email)
            user_url = reverse('profile', kwargs={'club_id': 0 ,'user_id': user.id})
            self.assertContains(response, user_url)
    
    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
