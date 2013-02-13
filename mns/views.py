#from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from mns.models import APISession
import json
import re


EMAIL_REGEX = r"^[\w\.\-\+]+@[\w\-\.]+\.[a-z]{2,3}$"


def index(request):
    return render(request, 'index.html', {})


def search(request):
    return render(request, 'search.html', {})


def my_profile(request):
    return render(request, 'profile.html', {})


def user(request, userid):
    return render(request, 'user.html', {})


def messages(request, userid):
    return render(request, 'messages.html', {})


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html', {})
