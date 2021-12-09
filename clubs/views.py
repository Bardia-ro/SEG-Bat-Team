<<<<<<< HEAD
from .models import User, Role, Club, Tournaments
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm, ClubCreatorForm
=======
from .models import User, Role, Club
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm, ClubCreatorForm, TournamentForm
>>>>>>> 758b37e734625ce3075f0c2136b822ed456d11bb
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helpers import get_is_user_member, only_current_user, redirect_authenticated_user, get_is_user_applicant, get_is_user_owner, get_is_user_officer

def request_toggle(request, user_id, club_id):

    currentUser = User.objects.get(id=user_id)
    club = Club.objects.get(id=club_id)
    user_is_owner = get_is_user_owner(club_id, request.user)

    try:
        role = Role.objects.get(user = currentUser, club = club)
        if user_is_owner:
            messages.add_message(request, messages.ERROR, "You must transfer ownership first.")
        else:
            role.delete()
    except:
        Role.objects.create(user = currentUser, club = club, role = 1)

    return redirect('club_page', club_id=club_id)

def club_page(request, club_id):

    club_list = request.user.get_clubs_user_is_a_member()
    club = Club.objects.get(id=club_id)
    club_members = Role.objects.filter(club=club, role=2)
    role_at_club = request.user.get_role_as_text_at_club(club_id)

    #following neesd to be refactored:
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

@redirect_authenticated_user
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                club_id = user.get_first_club_id_user_is_associated_with()
                return redirect('profile', club_id=club_id, user_id=request.user.id)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

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

def club_creator(request):
    if (request.user.is_authenticated != True):
        club_id = request.user.get_first_club_id_user_is_associated_with()
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    if request.method == 'POST':
        form = ClubCreatorForm(request.POST)
        if form.is_valid():
            club = form.save()
            club_id = request.user.get_first_club_id_user_is_associated_with()
            #attempt to add user as owner of the new club
            Role.objects.create(user = request.user, club = club, role = 4)
            return redirect('profile', club_id=club_id, user_id=request.user.id)
    else:
        form = ClubCreatorForm()

    return render(request, 'club_creator.html', {'form': form})

def create_tournament(request, club_id):
    role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id=request.user.id)
    if (role.role_name() == "Officer" and request.method == 'POST'):
        organiser = User.objects.filter(id = request.user.id).first()
        club = Club.objects.filter(id = club_id).first()
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(organiser, club)
            return redirect('profile', club_id=club_id, user_id=request.user.id)
    form = TournamentForm()
    return render(request, 'create_tournament.html', {'form': form, 'club_id': club_id})


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
    return render(request, 'edit_profile.html', {'form': form, 'club_id': club_id, 'user_is_member':user_is_member, 'club_list': club_list})

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
    return render(request, 'change_password.html', {'form': form, 'club_id': club_id, 'user_is_member':user_is_member, 'club_list': club_list})

@login_required
def profile(request, club_id, user_id):
    if club_id == 0:
        club_id = request.user.get_first_club_id_user_is_associated_with()
        if request.user.id == user_id:
            if club_id == 0:
                return render(request, 'profile.html', {'user': request.user, 'club_id': 0, 'user_is_member': False, 'is_current_user': True})
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

    request_user_is_member = request_user_role_at_club >= 2
    user_role_at_club = user.get_role_at_club(club_id)
    club_list = user.get_clubs_user_is_a_member()
    return render(request, 'profile.html', {'user': user, 'club_id': club_id, 'user_is_member': request_user_is_member, 'is_current_user': is_current_user, 'request_user_role': request_user_role_at_club, 'user_role': user_role_at_club, 'club_list': club_list})

<<<<<<< HEAD
=======
def club_page(request, club_id):
    club_list = request.user.get_clubs_user_is_a_member()
    club = Club.objects.get(id=club_id)
    club_members = Role.objects.filter(club=club, role=2)
    user_is_member = get_is_user_member(club_id, request.user)
    role_at_club = request.user.get_role_as_text_at_club(club_id)
    user_is_applicant = get_is_user_applicant(club_id, request.user)
    user_is_officer = get_is_user_officer(club_id, request. user)
    return render (request, 'club_page.html', {'club_id': club_id,'user_is_applicant': user_is_applicant, 'user_is_officer': user_is_officer, 'user_is_member':user_is_member, 'club': club, 'club_list': club_list, 'club_members': club_members, 'role_at_club': role_at_club})
>>>>>>> 758b37e734625ce3075f0c2136b822ed456d11bb

def member_list(request, club_id):
    if not request.user.get_is_user_associated_with_club(club_id):
        club_id = request.user.get_first_club_id_user_is_associated_with()
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    request_user_role_at_club = request.user.get_role_at_club(club_id)
    request_user_is_member = request_user_role_at_club >= 2
    if not request_user_is_member:
        return redirect('profile', club_id=club_id, user_id=request.user.id)

    users = User.objects.filter(club__id = club_id)
    club_list = request.user.get_clubs_user_is_a_member()
    return render(request, 'member_list.html', {'users': users, 'user_is_member': True, 'club_id': club_id, 'club_list': club_list})

@login_required
def approve_member(request, club_id, applicant_id):
    role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = applicant_id)
    officer_role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Applicant" and officer_role.role_name() == "Officer"):
        role.approve_membership()
    return redirect('pending_requests', club_id=club_id)

@login_required
def promote_member_to_officer(request, club_id, member_id):
    role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = member_id)
    owner_role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Member" and owner_role.role_name() == "Owner"):
        role.promote_member_to_officer()
    return redirect('profile', club_id=club_id, user_id=member_id)

@login_required
def demote_officer_to_member(request, club_id, officer_id):
    role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = officer_id)
    owner_role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = request.user.id)
    if (role.role_name() == "Officer" and owner_role.role_name() == "Owner"):
        role.demote_officer_to_member()
    return redirect('profile', club_id=club_id, user_id=officer_id)

@login_required
def transfer_ownership(request, club_id, new_owner_id):
    role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = request.user.id)
    new_owner_role = get_object_or_404(Role.objects.all(), club_id=club_id, user_id = new_owner_id)
    if (role.role_name() == "Owner" and new_owner_role.role_name() == "Officer"):
        role.change_owner(club_id, new_owner_id)
    return redirect('profile', club_id=club_id, user_id=new_owner_id)

@login_required
def club_list(request):
    user = User.objects.get(id=request.user.id)
    clubs = Club.objects.all()
    club_id = request.user.get_first_club_id_user_is_associated_with()
    club_list = user.get_clubs_user_is_a_member()
    return render(request, 'club_list.html', {'clubs': clubs, 'club_id': club_id, 'club_list': club_list})

def pending_requests(request,club_id):
    applicants = Role.objects.all().filter(role = 1).filter(club_id = club_id)
    # need applicants for a particular club
    return render(request, 'pending_requests.html', { 'club_id':club_id,'applicants' : applicants })


def apply_tournament_toggle(request, user_id, club_id, tournament_id):
    tournament = Tournaments.objects.get(id=tournament_id)
    tournament.toggle_apply(user_id)

    if tournament.is_time_left() == False:
        messages.add_message(request, messages.ERROR, "The deadline has passed.")

    if tournament.is_space() == False:
        messages.add_message(request, messages.ERROR, "This tournament is full.")

#    is_contender = tournament.is_contender(user_id)
    return redirect('club_page', club_id=club_id)
