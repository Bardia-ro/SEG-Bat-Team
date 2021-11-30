from django.shortcuts import redirect
from django.conf import settings

def get_is_user_member(user):
    if user.is_authenticated:
        return user.type != 'APPLICANT'
    return False

def only_current_user(func):
    def wrapper(request, user_id):
        current_user_id = request.user.id
        if current_user_id == user_id:
            return func(request, user_id)
        else:
            return redirect('profile', user_id=user_id)

    return wrapper

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function
