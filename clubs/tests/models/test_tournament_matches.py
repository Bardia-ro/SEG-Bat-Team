"""Test generation of tournament matches"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, EliminationMatch, User, UserInClub, Tournament, Match, GroupMatch, Group, GroupPoints, GroupMatchNextMatches

class TournamentMatchesTest(TestCase):
    """Test generation of tournament matches"""

    fixtures = [
        'clubs/tests/fixtures/tournament_match_club.json',
        'clubs/tests/fixtures/tournament_match_elim_matches.json',
        'clubs/tests/fixtures/tournament_match_groupmatches.json',
        'clubs/tests/fixtures/tournament_match_groupmatchnextmatches.json',
        'clubs/tests/fixtures/tournament_match_groups.json',
        'clubs/tests/fixtures/tournament_match_matches.json',
        'clubs/tests/fixtures/tournament_match_players.json',
        'clubs/tests/fixtures/tournament_match_tournaments.json',
        'clubs/tests/fixtures/tournament_match_userinclub.json',
        'clubs/tests/fixtures/tournament_match_grouppoints.json',
    ]

    def setUp(self):
        self.tournament = Tournament.objects.get(id=28)

    def test_generation_first_group_stage_matches_64_people(self):
        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G96'
        )
        self.assertEqual(groups.count(), 16)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 4)
            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 6)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 3)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 3)

    def test_generation_second_group_stage_matches_64_people(self):
        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )
        self.assertEqual(groups.count(), 8)

        group_stage_player_ids = []
        first_group_stage_winner_and_runner_up_ids = []

        first_group_stage_groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G96'
        )
        for group in first_group_stage_groups:
            group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
            first_group_stage_winner_and_runner_up_ids.append(group_points_objects[0].player.id)
            first_group_stage_winner_and_runner_up_ids.append(group_points_objects[1].player.id)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 4)

            for group_player in group_players:
                group_stage_player_ids.append(group_player.id)

            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 6)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 3)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 3)

        self.assertEqual(len(group_stage_player_ids), 32)
        group_stage_player_ids.sort()
        first_group_stage_winner_and_runner_up_ids.sort()
        self.assertEqual(group_stage_player_ids, first_group_stage_winner_and_runner_up_ids)

    def test_generation_first_group_stage_matches_48_people(self):
        self.tournament = Tournament.objects.get(id=29)

        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G96'
        )
        self.assertEqual(groups.count(), 16)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 3)
            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 3)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 2)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 2)

    def test_generation_second_group_stage_matches_48_people(self):
        self.tournament = Tournament.objects.get(id=29)

        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )
        self.assertEqual(groups.count(), 8)

        group_stage_player_ids = []
        first_group_stage_winner_and_runner_up_ids = []

        first_group_stage_groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G96'
        )
        for group in first_group_stage_groups:
            group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
            first_group_stage_winner_and_runner_up_ids.append(group_points_objects[0].player.id)
            first_group_stage_winner_and_runner_up_ids.append(group_points_objects[1].player.id)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 4)

            for group_player in group_players:
                group_stage_player_ids.append(group_player.id)

            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 6)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 3)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 3)

        self.assertEqual(len(group_stage_player_ids), 32)
        group_stage_player_ids.sort()
        first_group_stage_winner_and_runner_up_ids.sort()
        self.assertEqual(group_stage_player_ids, first_group_stage_winner_and_runner_up_ids)

    def test_generation_group_stage_matches_32_people(self):
        self.tournament = Tournament.objects.get(id=30)

        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )
        self.assertEqual(groups.count(), 8)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 4)
            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 6)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 3)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 3)

    def test_elim_rounds_have_correct_players_tournament_with_32_people(self):
        self.tournament = Tournament.objects.get(id=30)

        elim_rounds_player_ids = []
        elim_matches = EliminationMatch.objects.filter(tournament=self.tournament).order_by('match__number')
        for elim_match in elim_matches[0:8]:
            elim_rounds_player_ids.append(elim_match.match.player1.id)
            elim_rounds_player_ids.append(elim_match.match.player2.id)

        group_stage_winner_and_runner_up_ids = []
        
        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )

        for group in groups:
            group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
            group_stage_winner_and_runner_up_ids.append(group_points_objects[0].player.id)
            group_stage_winner_and_runner_up_ids.append(group_points_objects[1].player.id)

        elim_rounds_player_ids.sort()
        group_stage_winner_and_runner_up_ids.sort()
        self.assertEqual(elim_rounds_player_ids, group_stage_winner_and_runner_up_ids)

    def test_generation_group_stage_matches_24_people(self):
        self.tournament = Tournament.objects.get(id=31)

        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )
        self.assertEqual(groups.count(), 8)

        for group in groups:
            group_players = group.players.all()
            self.assertEqual(group_players.count(), 3)
            group_matches = GroupMatch.objects.filter(group=group)
            self.assertEqual(group_matches.count(), 3)
            for player in group_players:
                count = 0
                opponent_ids = []
                for group_match in group_matches:
                    if group_match.match.player1 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player2.id)
                    if group_match.match.player2 == player:
                        count += 1
                        opponent_ids.append(group_match.match.player1.id)

                self.assertEqual(count, 2)
                opponent_ids_set = set(opponent_ids)
                self.assertEqual(len(opponent_ids_set), 2)

    def test_elim_rounds_have_correct_players_tournament_with_24_people(self):
        self.tournament = Tournament.objects.get(id=31)

        elim_rounds_player_ids = []
        elim_matches = EliminationMatch.objects.filter(tournament=self.tournament).order_by('match__number')
        for elim_match in elim_matches[0:8]:
            elim_rounds_player_ids.append(elim_match.match.player1.id)
            elim_rounds_player_ids.append(elim_match.match.player2.id)

        group_stage_winner_and_runner_up_ids = []
        
        groups = Group.objects.filter(
            tournament=self.tournament,
            group_stage = 'G32'
        )

        for group in groups:
            group_points_objects = GroupPoints.objects.filter(group=group).order_by('-total_group_points')
            group_stage_winner_and_runner_up_ids.append(group_points_objects[0].player.id)
            group_stage_winner_and_runner_up_ids.append(group_points_objects[1].player.id)

        elim_rounds_player_ids.sort()
        group_stage_winner_and_runner_up_ids.sort()
        self.assertEqual(elim_rounds_player_ids, group_stage_winner_and_runner_up_ids)

    def test_generation_elim_matches_16_people(self):
        self.tournament = Tournament.objects.get(id=32)

        elim_matches = EliminationMatch.objects.filter(tournament = self.tournament).order_by('match__number')
        self.assertEqual(elim_matches.count(), 15)

        round_of_16_elim_matches = elim_matches[0:8]
        player_id_list=[]
        for elim_match in round_of_16_elim_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 16)

        quarter_final_matches = elim_matches[8:12]
        player_id_list=[]
        for elim_match in quarter_final_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 8)

        semi_final_matches = elim_matches[12:14]
        player_id_list=[]
        for elim_match in semi_final_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 4)

        final_match = elim_matches[14:15]
        player_id_list=[]
        for elim_match in final_match:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 2)

    def test_generation_elim_matches_8_people(self):
        self.tournament = Tournament.objects.get(id=33)

        elim_matches = EliminationMatch.objects.filter(tournament = self.tournament).order_by('match__number')
        self.assertEqual(elim_matches.count(), 7)

        quarter_final_matches = elim_matches[0:4]
        player_id_list=[]
        for elim_match in quarter_final_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 8)

        semi_final_matches = elim_matches[4:6]
        player_id_list=[]
        for elim_match in semi_final_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 4)

        final_match = elim_matches[6:7]
        player_id_list=[]
        for elim_match in final_match:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 2)

    def test_generation_elim_matches_4_people(self):
        self.tournament = Tournament.objects.get(id=34)

        elim_matches = EliminationMatch.objects.filter(tournament = self.tournament).order_by('match__number')
        self.assertEqual(elim_matches.count(), 3)

        semi_final_matches = elim_matches[0:2]
        player_id_list=[]
        for elim_match in semi_final_matches:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 4)

        final_match = elim_matches[2:3]
        player_id_list=[]
        for elim_match in final_match:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 2)

    def test_generation_elim_matches_2_people(self):
        self.tournament = Tournament.objects.get(id=35)

        elim_matches = EliminationMatch.objects.filter(tournament = self.tournament).order_by('match__number')
        self.assertEqual(elim_matches.count(), 1)

        final_match = elim_matches[0:1]
        player_id_list=[]
        for elim_match in final_match:
            player1_id = elim_match.match.player1.id
            player2_id = elim_match.match.player2.id             
            if player1_id not in player_id_list:
                player_id_list.append(player1_id)
            if player2_id not in player_id_list:
                player_id_list.append(player2_id)

        self.assertEqual(len(player_id_list), 2)

    def test_correct_players_in_certain_elim_match(self):
        self.tournament = Tournament.objects.get(id=34)

        elim_matches = EliminationMatch.objects.filter(tournament = self.tournament).order_by('match__number')
        self.assertEqual(elim_matches.count(), 3)

        self.assertEqual(elim_matches[2].match.player1, elim_matches[0].winner)
        self.assertEqual(elim_matches[2].match.player2, elim_matches[1].winner)