from django.shortcuts import redirect

def get_is_user_member(user):
    if user.is_authenticated:
        return user.role != 1
    return False

def only_current_user(func):
    def wrapper(request, user_id):
        current_user_id = request.user.id
        if current_user_id == user_id:
            return func(request, user_id)
        else:
            return redirect('profile', user_id=user_id)

    return wrapper