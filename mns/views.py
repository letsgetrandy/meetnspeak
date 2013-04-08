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
import api
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


def no_login():
    def decorator(fn):
        def inner_decorator(request, *args, **kwargs):
            if request.session.get('token'):
                return redirect(reverse('profile'))
            else:
                return fn(request, *args, **kwargs)
        return wraps(fn)(inner_decorator)
    return decorator


def index(request):
    context = {}
    return render(request, 'index.html', context)


@no_login()
def login(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # get login token
            backend = api_v1.MNSAPI()
            token = backend.login(email, password)
            request.session['token'] = token
            context['token'] = token

            # get notifications
            request.session['notifications'] = backend.get_notifications(token)

            return redirect(reverse('notifications'))
        #except api_v1.AccessDenied as err:
        except api.Unauthorized as e:
            context['error'] = str(e)
        #except Exception as err:
        #    context['error'] = str(err)
    return render(request, 'login.html', context)


@no_login()
def signup(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # get login token
            backend = api_v1.MNSAPI()
            token = backend.signup(email, password)
            request.session['token'] = token
            context['token'] = token

            # get notifications
            request.session['notifications'] = backend.get_notifications(token)

            return redirect(reverse('profile'))

        except api.BadRequest as e:
            context['error'] = str(e)
        except api.Forbidden as e:
            context['error'] = str(e)
    return render(request, 'signup.html', context)


@login_required()
def search(request):
    context = {}
    #token = request.session.get('token')
    return render(request, 'search.html', context)


@login_required()
def notifications(request):
    context = {}

    # re-check notifications
    backend = api_v1.MNSAPI()
    token = request.session.get('token')
    request.session['notifications'] = backend.get_notifications(token)

    return render(request, 'notifications.html', context)


@login_required()
def profile(request):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('name')
        form['dob'] = request.POST.get('dob')
        form['gender'] = request.POST.get('gender')
        form['hometown'] = request.POST.get('hometown')
        languages = []
        for (key, val) in request.POST.items():
            if key.startswith("lang_"):
                code = key[5:]
                languages.append("%s=%s" % (code, val))
        form['languages'] = ",".join(languages)
        backend.set_profile(token, **form)
    context['profile'] = backend.get_profile(token)
    context['lang_options'] = api_v1.language_name
    return render(request, 'profile.html', context)


@login_required()
def contacts(request):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    context['contacts'] = backend.get_contacts(token)
    return render(request, 'contacts.html', context)


@login_required()
def user(request, userid):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    context['profile'] = backend.get_user(token, 1)
    return render(request, 'user.html', context)


@login_required()
def messages(request, userid):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    context['messages'] = backend.get_messages(token, 1)
    return render(request, 'messages.html', context)


@login_required()
def settings(request):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    if request.method == 'POST':
        obj = {}
        obj['email'] = request.POST.get('email')
        obj['autoupdate'] = request.POST.get('autoupdate')

        backend.set_settings(token, **obj)
    obj = backend.get_settings(token)
    context.update(obj)
    return render(request, 'settings.html', context)


def logout(request):
    #auth.logout(request)
    if request.session.get('token'):
        del request.session['token']
    return redirect(reverse('login'))
    #return render(request, 'login.html', {})
