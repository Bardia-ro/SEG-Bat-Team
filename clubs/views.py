"""Views of the clubs app."""
from contextlib import nullcontext
from django.core.exceptions import ImproperlyConfigured
from .models import EliminationMatch, GroupMatch, User, UserInClub, Club, Tournament, Group, GroupPoints, Elo_Rating
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm, ClubCreatorForm, TournamentForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helpers import get_is_user_member,member_only,tournament_organiser_only,officer_owner_only,only_current_user, redirect_authenticated_user, get_is_user_applicant, get_is_user_owner, get_is_user_officer
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain, count

def request_toggle(request, user_id, club_id):
    """Toggles whether a user has applied to a club or left it."""

    currentUser = User.objects.get(id=user_id)
    club = Club.objects.get(id=club_id)
    user_is_owner = get_is_user_owner(club_id, request.user)

    try:
        role = UserInClub.objects.get(user = currentUser, club = club)
        if user_is_owner:
            messages.add_message(request, messages.ERROR, "You must transfer ownership first.")
        else:
            role.delete()
    except:
        UserInClub.objects.create(user = currentUser, club = club, role = 1)

    return redirect('club_page', club_id=club_id)


@login_required
def club_page(request, club_id):
    """View that shows relevant information of a club to a user depending on their role"""

    club_list = request.user.get_clubs_user_is_a_member()
    club = Club.objects.get(id=club_id)
    club_members = UserInClub.objects.filter(club=club, role=2)
    role_at_club = request.user.get_role_as_text_at_club(club_id)

    user_is_member = get_is_user_member(club_id, request.user)
    user_is_applicant = get_is_user_applicant(club_id, request.user)
    user_is_officer = get_is_user_officer(club_id, request. user)
    user_is_owner = get_is_user_owner(club_id, request.user)

    return render (request, 'club_page.html', {'club_id': club_id,
    'user_is_applicant': user_is_applicant,
    'user_is_officer': user_is_officer,
    'user_is_member':user_is_member,
    'club': club,
    'club_list': club_list,
    'club_members': club_members,
    'role_at_club': role_at_club,
    'user_is_owner': user_is_owner,
    })



class LoginProhibitedMixin:
    """Mixin redirects when a user is logged in """

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Refirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            url = self.redirect_when_logged_in_url()
            club_id = self.request.user.get_first_club_id_user_is_associated_with()
            return redirect('profile', club_id=club_id, user_id=self.request.user.id)
            return redirect(url)
        return super().dispatch(*args, **kwargs)

    def redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in"""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
            "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """View that handles log in."""

    http_method_names = ['get', 'post']

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or ''
        user = form.get_user()
        if user is not None:
            login(request, user)
            club_id = user.get_first_club_id_user_is_associated_with()
            return redirect(self.next or 'profile', club_id=club_id, user_id=request.user.id)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    logout(request)
    return redirect('home')

@redirect_authenticated_user
def home(request):
    return render(request, 'home.html')

@redirect_authenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            club_id = user.get_first_club_id_user_is_associated_with()
            return redirect('profile', club_id=club_id, user_id=request.user.id)
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form':form})

@login_required
def club_creator(request, club_id, user_id):
    if (request.user.is_authenticated != True):
        club_id = request.user.get_first_club_id_user_is_associated_with()
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    if request.method == 'POST':
        form = ClubCreatorForm(request.POST)
        if form.is_valid():
            club = form.save()
            UserInClub.objects.create(user = request.user, club = club, role = 4)
            return redirect('club_page', club_id=club.id)
    else:
        form = ClubCreatorForm()
    club_list = request.user.get_clubs_user_is_a_member()
    return render(request, 'club_creator.html', context={'form': form, 'club_id': club_id, 'user_id': user_id, 'club_list': club_list})

@login_required
@officer_owner_only
def create_tournament(request, club_id, user_id):
    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id=request.user.id)
    if ((role.role_name() == "Officer" or role.role_name() == "Owner")  and request.method == 'POST'):
        organiser = User.objects.filter(id = request.user.id).first()
        club = Club.objects.filter(id = club_id).first()
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(organiser, club)
            return redirect('club_page', club_id=club_id)
    else:
        form = TournamentForm()
    club_list = request.user.get_clubs_user_is_a_member()
    return render(request, 'create_tournament.html', context={'form': form, 'club_id': club_id, 'user_id': user_id, 'club_list': club_list})


@login_required
@only_current_user
def edit_profile(request, club_id, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', club_id=club_id, user_id=request.user.id)
    else:
        form = EditProfileForm(instance=user)
    user_is_member = get_is_user_member(club_id, request.user)
    club_list = user.get_clubs_user_is_a_member()
    return render(request, 'edit_profile.html', {'form': form, 'club_id': club_id, 'request_user_is_member':user_is_member, 'club_list': club_list})

@login_required
@only_current_user
def change_password(request, club_id, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', club_id=club_id, user_id=user.id)
    else:
        form = ChangePasswordForm(instance=user)
    user_is_member = get_is_user_member(club_id, request.user)
    club_list = user.get_clubs_user_is_a_member()
    return render(request, 'change_password.html', {'form': form, 'club_id': club_id, 'request_user_is_member':user_is_member, 'club_list': club_list})

@login_required
def profile(request, club_id, user_id):
    if club_id == 0:
        club_id = request.user.get_first_club_id_user_is_associated_with()
        if request.user.id == user_id:
            if club_id == 0:
                return render(request, 'profile.html', {'user': request.user, 'club_id': 0, 'request_user_is_member': False, 'is_current_user': True})
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    if not request.user.get_is_user_associated_with_club(club_id):
        club_id = request.user.get_first_club_id_user_is_associated_with()
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    user = User.objects.get(id=user_id)
    if not user.get_is_user_associated_with_club(club_id):
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    is_current_user = request.user.id == user_id
    request_user_role_at_club = request.user.get_role_at_club(club_id)

    if (request_user_role_at_club == 1 or request_user_role_at_club == 2) and not is_current_user:
        return redirect('profile', club_id=club_id, user_id=request.user.id)
    elo_rating = Elo_Rating.objects.filter(user = user).filter(club_id = club_id)
    max_elo = 0
    min_elo = 1000
    for ratings in elo_rating:
        if ratings.rating > max_elo:
            max_elo = ratings.rating
        if ratings.rating < min_elo:
            min_elo = ratings.rating
    if elo_rating.count() == 0:
        max_elo = min_elo
        min_elo = min_elo
    matchWon = Elo_Rating.objects.filter(user = user).filter(club_id = club_id).filter(result = user)
    matchDrawn = Elo_Rating.objects.filter(user = user).filter(club_id = club_id).filter(result__isnull = True)
    matchLost = elo_rating.count() - (matchWon.count() + matchDrawn.count())
    current_elo_rating = UserInClub.objects.filter(user = user_id).filter(club= club_id)
    current_elo = 0
    for rating in current_elo_rating:
        current_elo = rating.elo_rating
    tournaments = Tournament.objects.filter(players = user).filter(club_id = club_id)
    total_tournaments = Tournament.objects.filter(players = user).count()
    request_user_is_member = request_user_role_at_club >= 2
    user_role_at_club = user.get_role_at_club(club_id)
    club_list = user.get_clubs_user_is_a_member()
    #club_list = UserInClub.objects.filter(role=2, user=user)
    total_points = matchWon.count() + matchDrawn.count() * 0.5
    average_point = 0
    if elo_rating.count() > 0:
        average_point = total_points/elo_rating.count()
        average_point =  "{:.2f}".format(average_point)
    rate_of_change_elo = ((current_elo - 1000)/1000)*100

    return render(request, 'profile.html', {'user': user,
                           'club_id': club_id,
                           'request_user_is_member': request_user_is_member,
                           'is_current_user': is_current_user,
                           'request_user_role': request_user_role_at_club,
                           'user_role': user_role_at_club,
                           'club_list': club_list,
                           'elo_rating' : elo_rating,
                           'tournaments' : tournaments,
                           'matchLost' : matchLost,
                           'matchWon' : matchWon,
                           'max_elo' : max_elo,
                           'min_elo' : min_elo,
                           'matchDrawn' : matchDrawn,
                           'total_tournaments': total_tournaments,
                           'total_points' : total_points,
                           'current_elo' : current_elo,
                           'average_point' : average_point,
                           'rate_of_change_elo' : rate_of_change_elo })

@login_required
def member_list(request, club_id):
    """ List of all the members, officers and the owner in a given club. """

    if not request.user.get_is_user_associated_with_club(club_id):
        club_id = request.user.get_first_club_id_user_is_associated_with()
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    request_user_role_at_club = request.user.get_role_at_club(club_id)
    request_user_is_member = request_user_role_at_club >= 2
    if not request_user_is_member:
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    members = User.objects.filter(club__id = club_id, userinclub__role=2)
    officers = User.objects.filter(club__id = club_id, userinclub__role=3)
    users = User.objects.filter(club__id= club_id, userinclub__role=4).union(members, officers)
    club_list = request.user.get_clubs_user_is_a_member()
    return render(request, 'member_list.html', {'users': users, 'request_user_is_member': True, 'club_id': club_id, 'club_list': club_list})

@login_required
def approve_member(request, club_id, applicant_id):
    """ Owner and officers of a club can accept requests of applicants to join the club """

    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = applicant_id)
    officer_role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Applicant" and officer_role.role_name() == "Officer" or officer_role.role_name() == "Owner"):
        role.approve_membership()
    return redirect('pending_requests', club_id=club_id)

@login_required
def reject_member(request, club_id, applicant_id):
    """ Owner and officers of a club can reject requests of applicants to join the club """
    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = applicant_id)
    officer_role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Applicant" and officer_role.role_name() == "Officer" or officer_role.role_name() == "Owner"):
        role.reject_membership()
    return redirect('pending_requests', club_id=club_id)

@login_required
def promote_member_to_officer(request, club_id, member_id):
    """ Owner of a club can promote members of the same club to officers. """

    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = member_id)
    owner_role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Member" and owner_role.role_name() == "Owner"):
        role.promote_member_to_officer()
    return redirect('profile', club_id=club_id, user_id=member_id)

@login_required
def demote_officer_to_member(request, club_id, officer_id):
    """ Owner of a club can demote officers of the same club to members. """

    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = officer_id)
    owner_role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Officer" and owner_role.role_name() == "Owner"):
        role.demote_officer_to_member()
    return redirect('profile', club_id=club_id, user_id=officer_id)

@login_required
def transfer_ownership(request, club_id, new_owner_id):
    """ Owner of a club can transfer ownership to another officer of the same club. """

    role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = request.user.id)
    new_owner_role = get_object_or_404(UserInClub.objects.all(), club_id=club_id, user_id = new_owner_id)
    if (role.role_name() == "Owner" and new_owner_role.role_name() == "Officer"):
        role.change_owner(club_id, new_owner_id)
    return redirect('profile', club_id=club_id, user_id=new_owner_id)

@login_required
def club_list(request, club_id):
    """ List of all the created clubs. """

    user = User.objects.get(id=request.user.id)
    clubs = Club.objects.all()
    club_list = user.get_clubs_user_is_a_member()
    return render(request, 'club_list.html', {'clubs': clubs, 'club_id': club_id, 'club_list': club_list})

@login_required
@officer_owner_only
def pending_requests(request, club_id):
    """View all of the applicants to this club """

    applicant_id = UserInClub.objects.all().filter(role = 1).filter(club_id = club_id).values_list("user", flat=True)
    applicants = []
    for item in applicant_id:
        applicants.append(User.objects.get(id=item))
    club_list = request.user.get_clubs_user_is_a_member()
    return render(request, 'pending_requests.html', { 'club_id':club_id,'applicants' : applicants, 'club_list': club_list})

@login_required
@member_only
def apply_tournament_toggle(request, user_id, club_id, tournament_id):
    """View for toggling whether a member has applied to a tournament"""

    tournament = Tournament.objects.get(id=tournament_id)
    
    if tournament.is_time_left() == False:
        messages.add_message(request, messages.ERROR, "The deadline has passed.")

    if tournament.is_player(user_id) == False:
        if tournament.is_space() == False:
            messages.add_message(request, messages.ERROR, "This tournament is full.")
    tournament.toggle_apply(user_id)

    return redirect('club_page', club_id=club_id)

@login_required
@member_only
def match_schedule(request, club_id, tournament_id):
    club_list = request.user.get_clubs_user_is_a_member()
    tournament = Tournament.objects.get(id=tournament_id)

    g96_groups = Group.objects.filter(
        tournament=tournament,
        group_stage = 'G96'
    )

    g32_groups = Group.objects.filter(
        tournament=tournament,
        group_stage = 'G32'
    )

    num_players_in_tournament = tournament.player_count()
    if num_players_in_tournament > 16:
        num_players_elim_rounds = 16
    else:
        num_players_elim_rounds = num_players_in_tournament

    round_of_16_matches = EliminationMatch.objects.filter(
        tournament=tournament,
        match__number__lte = num_players_elim_rounds - 8,
        match__number__gte = num_players_elim_rounds - 15,
    ).order_by('match__number')
    quarter_final_matches = EliminationMatch.objects.filter(
        tournament=tournament,
        match__number__lte = num_players_elim_rounds - 4,
        match__number__gte = num_players_elim_rounds - 7,
    ).order_by('match__number')
    semi_final_matches = EliminationMatch.objects.filter(
        tournament=tournament,
        match__number__lte = num_players_elim_rounds - 2,
        match__number__gte = num_players_elim_rounds - 3,
    ).order_by('match__number')
    final_match = EliminationMatch.objects.filter(
        tournament=tournament,
        match__number = num_players_elim_rounds - 1
    ).order_by('match__number')

    return render(
        request,
        'match_schedule.html',
        {
            'club_id': club_id,
            'club_list': club_list,
            'tournament':tournament,
            'round_of_16_matches': round_of_16_matches,
            'quarter_final_matches': quarter_final_matches,
            'semi_final_matches': semi_final_matches,
            'final_match': final_match,
            'g32_groups': g32_groups,
            'g96_groups': g96_groups
        }
    )

@login_required
@tournament_organiser_only
def generate_next_matches(request, club_id, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    message = tournament.generate_next_matches()
    if message:
        messages.add_message(request, messages.ERROR, message)
    return redirect('match_schedule', club_id = club_id, tournament_id = tournament_id)

@login_required
@tournament_organiser_only
def enter_match_results(request, club_id, tournament_id, match_id):
    """Enter match results for a normal elimination round"""

    match = EliminationMatch.objects.get(id=match_id)
    if request.method=="POST":
        winner_id=request.POST['winner']
        winner = User.objects.get(id=winner_id)
        match.set_winner(winner)
        UserInClub.adjust_elo_rating(match,club_id,winner)
        match.save()
    return redirect('match_schedule', club_id = club_id, tournament_id = tournament_id)

@login_required
@tournament_organiser_only
def enter_match_results_groups(request, club_id, tournament_id, match_id):
    """Enter match results for group rounds. Adjusts the elo rating of the players"""

    group_match = GroupMatch.objects.get(id=match_id)
    match = group_match.match
    player_1 = match.player1
    player_2 = match.player2

    if request.method=="POST":
        result=request.POST['result']
        if result == 'draw':
            group_match.set_draw_points()
            UserInClub.adjust_elo_rating(group_match,club_id,"Draw")
        elif result == 'player1':
            group_match.player1_won_points()
            UserInClub.adjust_elo_rating(group_match,club_id,player_1)
        else:
            group_match.player2_won_points()
            UserInClub.adjust_elo_rating(group_match,club_id,player_2)
        group_match.save()
    return redirect('match_schedule', club_id = club_id, tournament_id = tournament_id)

@login_required
@tournament_organiser_only
def view_tournament_players(request,club_id, tournament_id):
    """View all the players in a tournament"""

    tournament = Tournament.objects.get(id=tournament_id)
    players = tournament.players.all()
    return render(request, 'contender_in_tournaments.html', {'players' : players, 'club_id': club_id, 'tournament_id': tournament_id, 'tournament': tournament})

@login_required
@tournament_organiser_only
def remove_a_player(request,user_id,club_id,tournament_id):
    """Removes a player from a tournament."""

    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.valid_player_count() == False:
        tournament.remove_player(user_id)
    else:
        messages.add_message(request, messages.ERROR, "You cannot remove any more players")
    return redirect('view_tournament_players', club_id = club_id, tournament_id = tournament_id)
