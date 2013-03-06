#from django.conf import settings
#from django.contrib import auth
from django.core.urlresolvers import reverse
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.shortcuts import render, redirect
#from mns.models import APISession
from functools import wraps
#import json
#import re
import api_v1
#import sys


EMAIL_REGEX = r"^[\w\.\-\+]+@[\w\-\.]+\.[a-z]{2,3}$"


def login_required():
    def decorator(fn):
        def inner_decorator(request, *args, **kwargs):
            if not request.session.get('token'):
                return redirect(reverse('login'))
            else:
                return fn(request, *args, **kwargs)
        return wraps(fn)(inner_decorator)
    return decorator


def index(request):
    context = {}
    return render(request, 'index.html', context)


def login(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # get login token
            api = api_v1.MNSAPI()
            token = api.login(email, password)
            request.session['token'] = token
            context['token'] = token

            # get notifications
            api = api_v1.MNSAPI()
            request.session['notifications'] = api.get_notifications(token)

            return redirect(reverse('notifications'))
        except api_v1.AccessDenied as err:
            context['error'] = str(err)
        #except Exception as err:
        #    context['error'] = str(err)
    return render(request, 'login.html', context)


def signup(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #try:
        # get login token
        api = api_v1.MNSAPI()
        token = api.signup(email, password)
        request.session['token'] = token
        context['token'] = token

        # get notifications
        api = api_v1.MNSAPI()
        request.session['notifications'] = api.get_notifications(token)

        return redirect(reverse('profile'))
        #except:
        #    context['error'] = True
    return render(request, 'signup.html', context)


@login_required()
def search(request):
    context = {}
    #token = request.session.get('token')
    return render(request, 'search.html', context)


@login_required()
def notifications(request):
    context = {}
    #token = request.session.get('token')
    return render(request, 'notifications.html', context)


@login_required()
def profile(request):
    context = {}
    #token = request.session.get('token')
    return render(request, 'profile.html', context)


@login_required()
def contacts(request):
    context = {}
    token = request.session.get('token')
    api = api_v1.MNSAPI()
    context['contacts'] = api.get_contacts(1, token)
    return render(request, 'contacts.html', context)


@login_required()
def user(request, userid):
    context = {}
    token = request.session.get('token')
    api = api_v1.MNSAPI()
    context['profile'] = api.get_profile(1, token)
    return render(request, 'user.html', context)


@login_required()
def messages(request, userid):
    context = {}
    token = request.session.get('token')
    api = api_v1.MNSAPI()
    context['messages'] = api.get_messages(1, token)
    return render(request, 'messages.html', context)


@login_required()
def settings(request):
    context = {}
    token = request.session.get('token')
    api = api_v1.MNSAPI()
    if request.method == 'POST':
        obj = {}
        obj['email'] = request.POST.get('email')
        obj['autoupdate'] = request.POST.get('autoupdate')

        api.set_settings(token, **obj)
    obj = api.get_settings(token)
    context.update(obj)
    return render(request, 'settings.html', context)


def logout(request):
    #auth.logout(request)
    if request.session.get('token'):
        del request.session['token']
    return redirect(reverse('login'))
    #return render(request, 'login.html', {})
