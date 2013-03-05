from django.conf import settings


def request_session(request):
    notifications = request.session.get('notifications')
    return {'notifications': notifications}
