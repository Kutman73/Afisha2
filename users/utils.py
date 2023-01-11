
def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None


def get_superuser_from_request(request):
    return request.user.is_superuser if not request.user.is_superuser else None
