from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class MemberListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('member_list', kwargs={'club_id': 0})
        self.user = User.objects.get(email='johndoe@example.org')

    def test_member_list_url(self):
        self.assertEqual(self.url,f'/member_list/0/')

    def test_get_member_list(self):
        self.client.login(email=self.user.email, password='Password123')
        self._create_test_users(15-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15-1):
            self.assertContains(response, f'user{user_id}@test.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(email=f'user{user_id}@test.org')
            user_url = reverse('profile', kwargs={'club_id': 0 ,'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_users(self, user_count=10):
        for user_id in range(user_count):
            User.objects.create_user(
                email=f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience='class D',
                personal_statement=f'Personal_Statement{user_id}'
            )