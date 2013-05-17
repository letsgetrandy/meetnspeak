from django.conf import settings
#from django.contrib import auth
from django.core.urlresolvers import reverse
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
#from mns.models import APISession
from functools import wraps
from mns import img_helper
import json
#import re
import api
import api_v1
import StringIO
#import sys


EMAIL_REGEX = r"^[\w\.\-\+]+@[\w\-\.]+\.[a-z]{2,3}$"


def login_required():
    def decorator(fn):
        def inner_decorator(request, *args, **kwargs):
            if not request.session.get('token'):
                return redirect(reverse('login'))
            else:
                try:
                    return fn(request, *args, **kwargs)
                except api.BadRequest as e:
                    if e.token_expired:
                        del request.session['token']
                        context = {
                                "error": "Your session has expired."
                                }
                        return render(request, "login.html", context)
                    else:
                        return render(request, "500.html", {})
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
            request.session['profile'] = backend.get_profile(token)
            context['token'] = token

            # get notifications
            request.session['notifications'] = backend.get_notifications(token)

            return redirect(reverse('notifications'))
        #except api_v1.AccessDenied as err:
        except api.Unauthorized as e:
            context['error'] = str(e)
        #except Exception as err:
        #    context['error'] = str(err)
        context['email'] = email
        context['password'] = password
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
        context['email'] = email
        context['password'] = password
    return render(request, 'signup.html', context)


@login_required()
def search(request):
    profile = request.session.get("profile", "")
    context = {
            'profile': profile
        }
    if profile:
        mylangs = [l["code"] for l in profile.languages]
        context["mylangs"] = json.dumps(mylangs)
    #token = request.session.get('token')
    #print >> sys.stderr, context
    return render(request, 'search.html', context)


@login_required()
def search_ajax(request):
    # don't allow my service to get hijacked
    if not settings.DEBUG:
        from urlparse import urlparse
        u = urlparse(request.META.get('HTTP_REFERER'))
        if u.hostname not in [
                'localhost',
                'www.spikizi.com',
                'spikizi.herokuapp.com'
            ]:
            raise Http404

    #context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    form = {}
    form['location'] = request.GET.get('location')
    form['languages'] = request.GET.get('languages')
    if token:
        form['token'] = token
    result = backend.search(**form)
    return HttpResponse(json.dumps(result), mimetype='application/json')


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
        form['age'] = request.POST.get('age', '')
        form['gender'] = request.POST.get('gender')
        form['hometown'] = request.POST.get('hometown')
        form['website'] = request.POST.get('website')
        form['twitter'] = request.POST.get('twitter')
        form['location'] = request.POST.get('location')
        form['location_name'] = request.POST.get('location_name')
        languages = []
        for (key, val) in request.POST.items():
            if key.startswith("lang_"):
                code = key[5:]
                languages.append("%s=%s" % (code, val))
        if languages:
            form['languages'] = ",".join(languages)
        #print >> sys.stderr, form
        backend.set_profile(token, **form)
    p = backend.get_profile(token)
    #print >> sys.stderr, p
    context['profile'] = p
    request.session['profile'] = p
    context['lang_options'] = api_v1.language_name
    return render(request, 'profile.html', context)


@login_required()
def image(request):
    i = request.FILES['image']
    imagefile = StringIO.StringIO(i.read())
    img = img_helper.prepare(imagefile)

    #filename = hashlib.md5(imagefile.getvalue()).hexdigest() + ".jpg"
    name = request.session['profile'].id
    filename = img_helper.save_thumbnail(name, img, 100)

    data = json.dumps({"image": filename})
    return HttpResponse(data, mimetype='application/json')


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
    context['profile'] = backend.get_user(token, userid)
    return render(request, 'user.html', context)


@login_required()
def messages(request, userid):
    context = {}
    token = request.session.get('token')
    backend = api_v1.MNSAPI()
    context['messages'] = backend.get_messages(token, userid)
    return render(request, 'messages.html', context)


@login_required()
def user_settings(request):
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
