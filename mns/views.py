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


def login(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.GET.get('email')
        password = request.GET.get('password')
        try:
            api = api_v1.MNSAPI()
            token = api.login(email, password)
            request.session['token'] = token
            context['token'] = token
        except:
            context['error'] = "No user was found with that combination of username and password."
    return render(request, 'login.html', context)


def signup(request):
    context = {}
    if request.session.get('token'):
        context['error'] = "already logged in"
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #try:
        api = api_v1.MNSAPI()
        token = api.signup(email, password)
        request.session['token'] = token
        context['token'] = token
        #except:
        #    context['error'] = True
    return render(request, 'signup.html', context)


def search(request):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    return render(request, 'search.html', context)


def profile(request):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    return render(request, 'profile.html', context)


def contacts(request):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    api = api_v1.MNSAPI()
    context['contacts'] = api.get_contacts(1)
    return render(request, 'contacts.html', context)


def user(request, userid):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    api = api_v1.MNSAPI()
    context['profile'] = api.get_profile(1)
    return render(request, 'user.html', context)


def messages(request, userid):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    api = api_v1.MNSAPI()
    context['messages'] = api.get_messages(1)
    return render(request, 'messages.html', context)


def settings(request):
    if not request.session.get('token'):
        context = {'error': 'login required'}
        return render(request, 'login.html', context)
    context = {}
    return render(request, 'settings.html', context)


def logout(request):
    #auth.logout(request)
    del request.session['token']
    return render(request, 'logout.html', {})
