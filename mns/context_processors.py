from django.conf import settings


def request_session(request):
    notifications = request.session.get('notifications')
    profile = request.session.get('profile')
    return {
            'notifications': notifications,
            'profile': profile,
        }


def site_settings(request):
    return {'settings': settings}
