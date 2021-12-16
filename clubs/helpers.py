from django.shortcuts import redirect
from clubs.models import Role, Tournament

def redirect_authenticated_user(func):
    def wrapper(request):
        if request.user.is_authenticated:
            club_id = request.user.get_first_club_id_user_is_associated_with()
            return redirect('profile', club_id=club_id, user_id=request.user.id)
        else:
            return func(request)
    return wrapper

def officer_owner_only(func):
    """Redirects a user back to their profile if they try to access an officer/owner only page"""
    def wrapper(request, club_id,**options):
            if get_is_user_officer(club_id, request.user) or get_is_user_owner(club_id, request.user):
                return func(request,club_id=club_id,**options)
            else:
                club_id = request.user.get_first_club_id_user_is_associated_with()
                return redirect('profile', club_id=club_id, user_id=request.user.id)
    return wrapper

def organiser_only(func):
    def wrapper(request, club_id,**options):
            if get_is_user_officer(club_id, request.user) or get_is_user_owner(club_id, request.user):
                return func(request,club_id=club_id,**options)
            else:
                club_id = request.user.get_first_club_id_user_is_associated_with()
                return redirect('profile', club_id=club_id, user_id=request.user.id)
    return wrapper


def only_current_user(func):
    def wrapper(request, club_id, user_id):
        current_user_id = request.user.id
        if current_user_id == user_id:
            return func(request, club_id, user_id)
        else:
            return redirect('profile', club_id=club_id, user_id=user_id)
    return wrapper


def get_is_user_member(club_id, user):
    """Returns whether a user is a member of this club"""
    if user.is_authenticated:
        try:
            return Role.objects.get(club__id=club_id, user__id=user.id).role >= 2
        except: #add error
            return False
    return False

def get_is_user_organiser(club_id, user):
    """Returns whether a user is a member of this club"""
    if user.is_authenticated:
        try:
            return Role.objects.get(club__id=club_id, user__id=user.id).role >= 2
        except: #add error
            return False
    return False

def get_is_user_owner(club_id, user):
    """Returns whether a user is an owner of this club"""
    if user.is_authenticated:
        try:
            return Role.objects.get(club__id=club_id, user__id=user.id).role == 4
        except: #add error
            return False
    return False

def get_is_user_officer(club_id, user):
    """Returns whether a user is an officer of this club"""
    if user.is_authenticated:
        try:
            return Role.objects.get(club__id=club_id, user__id=user.id).role == 3
        except: #add error
            return False
    return False

def get_is_user_applicant(club_id, user):
    """Returns whether a user is an applicant of this club"""
    if user.is_authenticated:
        try:
            return Role.objects.get(club__id=club_id, user__id=user.id).role == 1
        except: #add error
            return False
    return False
