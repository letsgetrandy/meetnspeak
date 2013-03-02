from django.conf import settings


def request_session(request):
    return {'notifications': request.session['notifications']}
