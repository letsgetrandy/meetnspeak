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


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html', {})
