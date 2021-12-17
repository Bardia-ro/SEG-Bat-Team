from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Tournament
from clubs.tests.helpers import reverse_with_next

class TournamentPlayersTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/default_tournament.json']

    def setUp(self):
        self.url = reverse('view_tournament_players', kwargs={"club_id": 0, "tournament_id": 1})
        self.user = User.objects.get(pk=5)
        self.tournament = Tournament.objects.get(pk=1)

    def test_member_list_url(self):
        self.assertEqual(self.url,'/view_tournament_players/0/1/')

    def test_view_tournament_players(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contender_in_tournaments.html')
        for player in self.tournament.players.all():
            user=player
            club_url = reverse('profile', kwargs={'club_id': 0 ,'user_id': user.id})
            self.assertContains(response, club_url)
    
    def test_view_tournament_player_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_remove_players_toggle_rejects_when_capacity_valid(self):
        self.client.login(email=self.user.email, password='Password123')
        before_count=self.tournament.players.all().count()
        url= reverse('remove_a_player', kwargs={ "user_id":2,"club_id": 0, "tournament_id": 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count=self.tournament.players.all().count()
        self.assertEqual(after_count, before_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_remove_players_toggle(self):
        self.client.login(email=self.user.email, password='Password123')
        before_count=self.tournament.players.all().count()
        url= reverse('remove_a_player', kwargs={ "user_id":2,"club_id": 0, "tournament_id": 2})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count=self.tournament.players.all().count()
        self.assertEqual(after_count, before_count)
