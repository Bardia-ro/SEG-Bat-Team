from .models import User, Role
from django.db.models import Model
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm
from django.core.exceptions import ObjectDoesNotExist
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
                return redirect('profile', club_id=1, user_id=request.user.id) #change club_id value!!
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
            return redirect('profile', user_id=request.user.id)
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
    try:
        request_user_role_at_club = Role.objects.get(club__id=club_id, user__id=request.user.id).role
    except: # add in exception type
        #Change!!!
        return redirect('home')
    if (request_user_role_at_club == 1 or request_user_role_at_club == 2) and user_id != request.user.id:
        return redirect('profile', user_id=request.user.id)
    user = User.objects.get(id=user_id)
    user_is_member = request_user_role_at_club >= 2
    is_current_user = request.user.id == user_id
    return render(request, 'profile.html', {'user': user, 'club_id': club_id, 'user_is_member': user_is_member, 'is_current_user': is_current_user})

    return render(request, 'sign_up.html', {'form': form})

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