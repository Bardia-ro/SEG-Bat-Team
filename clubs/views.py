from .models import User
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helpers import get_is_user_member, only_current_user, redirect_authenticated_user

def log_in(request):
    redirect_authenticated_user(request)

    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                club_id = user.get_first_club_id_user_is_associated_with()
                return redirect('profile', club_id=club_id, user_id=request.user.id)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    redirect_authenticated_user(request)
    return render(request, 'home.html')

def sign_up(request):
    redirect_authenticated_user(request)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            club_id = user.get_first_club_id_user_is_associated_with()
            return redirect('profile', club_id=club_id, user_id=request.user.id)
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

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
    return render(request, 'edit_profile.html', {'form': form, 'club_id': club_id, 'user_is_member':user_is_member})

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
    return render(request, 'change_password.html', {'form': form, 'club_id': club_id, 'user_is_member':user_is_member})

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
    return render(request, 'profile.html', {'user': user, 'club_id': club_id, 'user_is_member': request_user_is_member, 'is_current_user': is_current_user})

def member_list(request, club_id):
   users = User.objects.all()
   return render(request, 'member_list.html', {'users': users})

def approve_member(request, club_id, user_id):
    user = get_object_or_404(User.objects.filter(is_superuser=False), pk = user_id)
    user.approve_membership()
    return render(request, 'profile.html', {'user' : user})

def promote(request, club_id, user_id):
    user = get_object_or_404(User.objects.filter(is_superuser=False), pk = user_id)
    user.promotion_member_demotion_owner()
    return render(request, 'profile.html', {'user' : user})

def demote(request, club_id, user_id):
    user = get_object_or_404(User.objects.filter(is_superuser=False), pk = user_id)
    user.demotion()
    return render(request, 'profile.html', {'user' : user})

def transferownership(request, club_id, user_id, request_user_id):
    user = get_object_or_404(User.objects.filter(is_superuser=False), pk = user_id)
    user.change_owner(request_user_id)
    return render(request, 'profile.html', {'user' : user})