from .models import User
from .forms import SignUpForm, LogInForm
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

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})
