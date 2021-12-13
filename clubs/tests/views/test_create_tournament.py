"""Tests of the create tournament view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from clubs.forms import TournamentForm
from clubs.models import Tournaments, User
from clubs.tests.helpers import LogInTester

class CreateTournamentViewTestCase(TestCase, LogInTester):
    """Tests of the club creator view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json'
                ]

    def setUp(self):
        self.user = User.objects.get(email='jackdoe@example.org')
        self.url = reverse('create_tournament', kwargs={"club_id": 0, "user_id": self.user.id})
        self.form_input = {
            'name': 'Tournament A',
            'description': 'This is the description',
            'capacity': 4,
            'deadline': '2021-01-12 14:12:06'
        }
        
    def test_create_tournament_url(self):
        self.assertEqual(self.url,'/create_tournament/0/4/')

    def test_get_create_tournament(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_tournament.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TournamentForm))
        self.assertFalse(form.is_bound)
    
    def test_non_logged_in_user_gets_create_tournament(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/create_tournament/0/4/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')
    
    
    def test_unsuccessful_create_tournament(self):
        self.client.login(email='jackdoe@example.org', password='Password123')
        self.form_input['name'] = ' '
        before_count = Tournaments.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Tournaments.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_tournament.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TournamentForm))
        self.assertTrue(form.is_bound)
    
    def test_successful_create_tournament(self):
        self.client.login(email='jackdoe@example.org', password='Password123')
        before_count = Tournaments.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Tournaments.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('club_page', kwargs={'club_id': 0})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_page.html')
        tournament = Tournaments.objects.get(name='Tournament A')
        self.assertEqual(tournament.name, 'Tournament A')
        self.assertEqual(tournament.capacity, 4)
        # self.assertEqual(tournament.deadline, '2021-01-12 14:12:06')
