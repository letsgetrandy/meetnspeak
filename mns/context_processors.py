from django.conf import settings


def request_session(request):
    notifications = request.session.get('notifications')
    return {'notifications': notifications}


def site_settings(request):
    return {'settings': settings}
