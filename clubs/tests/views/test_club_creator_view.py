"""Tests of the club creator view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from clubs.forms import ClubCreatorForm
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester

class ClubCreatorViewTestCase(TestCase, LogInTester):
    """Tests of the club creator view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json'
                ]

    def setUp(self):
        self.user = User.objects.get(email='janedoe@example.org')
        self.url = reverse('club_creator', kwargs={"club_id": 1, "user_id": self.user.id})
        self.form_input = {
            'name': 'New Club',
            'city': 'London',
            'description': 'This is the description'
        }
        
    def test_club_creator_url(self):
        self.assertEqual(self.url,'/club_creator/1/2/')

    def test_get_club_creator(self):
        self.client.login(email='janedoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_creator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ClubCreatorForm))
        self.assertFalse(form.is_bound)
    
    def test_non_logged_in_user_gets_club_creator(self):
        response = self.client.get(self.url, follow=True)
        expected_url = '/log_in/?next=/club_creator/1/2/'
        self.assertRedirects(response, expected_url)
        self.assertTemplateUsed(response, 'log_in.html')
    
    
    def test_unsuccessful_club_creator(self):
        self.client.login(email='janedoe@example.org', password='Password123')
        self.form_input['name'] = ' '
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_creator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ClubCreatorForm))
        self.assertTrue(form.is_bound)
    
    def test_successful_club_creator(self):
        self.client.login(email='janedoe@example.org', password='Password123')
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('club_page', kwargs={'club_id': 0})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_page.html')
        club = Club.objects.get(name='New Club')
        self.assertEqual(club.name, 'New Club')
        self.assertEqual(club.description, 'This is the description')
        self.assertEqual(club.city, 'London')
