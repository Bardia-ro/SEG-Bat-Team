from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import reverse_with_next

class ClubListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_tournament.json']

    def setUp(self):
        self.url = reverse('club_list', kwargs={'club_id': 0})
        self.user = User.objects.get(email='johndoe@example.org')

    def test_member_list_url(self):
        self.assertEqual(self.url,'/club_list/0/')

    def test_get_member_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        for club in self.clubs:
            club=club
            self.assertContains(response, club.name)
            self.assertContains(response, club.description)
            self.assertContains(response, club.location)
            club_url = reverse('club_page', kwargs={'club_id': club.id})
            self.assertContains(response, club_url)
    
    def test_get_member_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
