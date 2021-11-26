from .models import User
from .forms import SignUpForm, LogInForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') #change where this redirects to
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def member_list(request):
    queryset = User.objects.all()
    context = {"object_list": queryset}
    return render(request, 'member_list.html', context)

def roles(request):
    # gets list of users to promote
    queryset = User.objects.exclude(type = 'APPLICANT')
    context = {"user_list": queryset}
    # promotes the selected user to officer
    #if request.method == 'POST':
        #username_to_get = SUBMITTED DATA
        #user_to_change = User.objects.get(username=username_to_get)
        #user_to_change.type = 'OFFICER'
        #return redirect('promote-demote')

    return render(request, 'promote-demote.html', context)

