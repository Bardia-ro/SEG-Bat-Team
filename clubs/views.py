from .models import User
from .forms import SignUpForm, LogInForm, EditProfileForm, ChangePasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helpers import get_is_user_member, only_current_user, login_prohibited




class LogInView(View):
    """View that handles log in"""

    http_method_names = ['get', 'post']

    @method_decorator(login_prohibited)
    def dispatch(self, request):
        return super().dispatch(request)

    def get(self, request):
        """Display log in template"""
        next = request.GET.get('next') or ''
        form = LogInForm()
        user_is_member = get_is_user_member(request.user)
        return render(request, 'log_in.html', {'form': form, 'next': next,'user_is_member':user_is_member})

    def post(self, request):
        """Handle login attempt"""
        form = LogInForm(request.POST)
        next = request.GET.get('next') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', user_id=request.user.id)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        form = LogInForm()
        user_is_member = get_is_user_member(request.user)
        return render(request, 'log_in.html', {'form': form, 'next': next,'user_is_member':user_is_member})


def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', user_id=request.user.id)
    else:
        form = SignUpForm()
    user_is_member = get_is_user_member(request.user)
    return render(request, 'sign_up.html', {'form': form, 'user_is_member':user_is_member})

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
    user_is_member = get_is_user_member(request.user)
    return render(request, 'edit_profile.html', {'form': form, 'user_is_member':user_is_member})

@login_required
@only_current_user
def change_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', user_id=user.id)
    else:
        form = ChangePasswordForm(instance=user)
    user_is_member = get_is_user_member(request.user)
    return render(request, 'change_password.html', {'form': form, 'user_is_member':user_is_member})

@login_required
def profile(request, user_id):
    if (request.user.type == "APPLICANT" or request.user.type == "MEMBER") and user_id != request.user.id:
        return redirect('profile', user_id=request.user.id)
    user = User.objects.get(id=user_id)
    user_is_member = get_is_user_member(request.user)
    is_current_user = request.user.id == user_id
    return render(request, 'profile.html', {'user': user, 'user_is_member': user_is_member, 'is_current_user': is_current_user})

    return render(request, 'sign_up.html', {'form': form})

@login_required
def member_list(request):
    queryset = User.objects.all()
    context = {"object_list": queryset}
    return render(request, 'member_list.html', context)
