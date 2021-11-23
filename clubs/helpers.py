def get_is_user_member(user):
    if user.is_authenticated:
        return user.type != 'APPLICANT'
    return False