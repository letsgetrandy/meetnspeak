#from django.conf import settings
from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.shortcuts import render, redirect
#from mns.models import APISession
#import json
#import re
import api_v1
#import sys


EMAIL_REGEX = r"^[\w\.\-\+]+@[\w\-\.]+\.[a-z]{2,3}$"


def index(request):
    context = {}

    # TODO: move this to the login handler
    api = api_v1.MNSAPI()
    request.session['notifications'] = api.get_notifications(1)

    return render(request, 'index.html', context)


def search(request):
    context = {}
    return render(request, 'search.html', context)


def profile(request):
    context = {}
    return render(request, 'profile.html', context)


def contacts(request):
    context = {}
    api = api_v1.MNSAPI()
    context['contacts'] = api.get_contacts(1)
    return render(request, 'contacts.html', context)


def user(request, userid):
    context = {}
    api = api_v1.MNSAPI()
    context['profile'] = api.get_profile(1)
    return render(request, 'user.html', context)


def messages(request, userid):
    context = {}
    api = api_v1.MNSAPI()
    context['messages'] = api.get_messages(1)
    return render(request, 'messages.html', context)


def settings(request):
    context = {}
    return render(request, 'settings.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html', {})
