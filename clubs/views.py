from .models import User
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', user_id=request.user.id)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html', {'user': request.user})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', user_id=request.user.id)
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def only_current_user(func):
    def wrapper(request, user_id):
        current_user_id = request.user.id
        if current_user_id == user_id:
            return func(request, user_id)
        else:
            return redirect('profile', user_id=user_id)

    return wrapper

@login_required
@only_current_user
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
@only_current_user
def change_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})
