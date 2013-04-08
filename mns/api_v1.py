from django.core.urlresolvers import reverse
from django.conf import settings
import json
import httplib
import urllib
import sys
import api


language_name = {
        'EN': 'English',
        'FR': 'French',
        'GR': 'Greek',
        'IT': 'Italian',
        'PL': 'Polish',
        'RU': 'Russian',
        'SP': 'Spanish',
    }


language_level = [
        'None',
        'Beginner',      # 1
        'Beginner',
        'Intermediate',  # 3
        'Intermediate',
        'Advanced',      # 5
        'Advanced',
        'Fluent',        # 7
        'Fluent',
        'Native',        # 9
        'Native',
    ]


class Notification(object):

    def __init__(self, *args, **kwargs):
        self.text = kwargs['message']
        self.target = kwargs['target']
        self.sender = kwargs['sender']
        self.readdate = kwargs['readdate']

    @property
    def target_url(self):
        if self.target == 1:
            return reverse("profile")
        else:
            return "#"


class Contact:

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


class Message:

    def __init__(self, *args, **kwargs):
        self.text = kwargs['text']


class Profile:

    def __init__(self, *args, **kwargs):
        print >> sys.stderr, kwargs
        #self.id = kwargs['id']
        self.name = kwargs['name'] or ""
        self.age = kwargs['age'] or ""
        self.gender = kwargs['gender'] or ""
        self.hometown = kwargs['hometown'] or ""
        self.languages = []
        for lang, lev in kwargs['languages'].items():
            self.languages.append({
                    'code': lang,
                    'name': language_name[lang.upper()],
                    'level': lev,
                    'levelname': language_level[lev],
                })

    @property
    def male(self):
        return self.gender > 0


class APIException(Exception):
    pass


class ExpiredToken(Exception):
    pass


class BadLogin(Exception):
    pass


class APIBase(object):
    def request(self, endpoint, method='GET', data=None, head=None):
        headers = {
                'Accept': 'text/json',
            }
        if head:
            headers.update(head)
        conn = httplib.HTTPConnection(settings.APIHOST)
        if data:
            encdata = urllib.urlencode(data)
            if method == 'GET':
                endpoint = '%s?%s' % (endpoint, encdata)
                encdata = None
        else:
            encdata = None
        if method == 'POST':
            headers['Content-type'] = 'application/x-www-form-urlencoded'
        conn.request(method, endpoint, encdata, headers)
        resp = conn.getresponse()
        st = resp.status
        d = resp.read()
        print >> sys.stderr, d
        conn.close
        j = json.loads(d)
        if st == 400:
            raise api.BadRequest(j['error'])
        elif st == 401:
            raise api.Unauthorized(j['error'])
        elif st == 403:
            raise api.Forbidden(j['error'])
        elif st == 404:
            raise api.NotFound(j['error'])
        elif st == 405:
            raise api.MethodNotAllowed(j['error'])
        #TODO:500 error
        #elif st == 500:
        #   raise api.
        elif st != 200:
            raise Exception(d)
        #elif j.get('token_expired'):
        #    raise ExpiredToken(j['error'])
        #elif j.get('bad_login'):
        #    raise BadLogin(j['error'])
        elif not j['success']:
            raise APIException(j['error'])
        return j

    def get(self, endpoint, data=None, head=None):
        return self.request(endpoint, data=data, head=head)

    def post(self, endpoint, data=None, head=None):
        return self.request(endpoint, method='POST', data=data, head=head)


class MNSAPI(APIBase):

    def signup(self, email, password):
        form = {'email': email, 'password': password}
        data = self.post('/api/1.0/signup/', data=form)
        return data['token']

    def login(self, email, password):
        form = {'email': email, 'password': password}
        data = self.post('/api/1.0/login/', data=form)
        return data['token']

    def get_notifications(self, token):
        data = self.get('/api/1.0/notifications/',
                head={'token': token})
        result = []
        for n in data['notifications']:
            result.append(Notification(**n))
        return result

    def get_settings(self, token):
        data = self.get('/api/1.0/settings/', head={'token': token})
        result = data
        return result

    def set_settings(self, token, *args, **kwargs):
        form = kwargs
        data = self.post('/api/1.0/settings/', head={'token': token}, data=form)
        result = data
        return result

    def get_contacts(self, token):
        data = self.get('/api/1.0/contacts/', head={'token': token})
        result = []
        for c in data['contacts']:
            result.append(Contact(**c))
        return result

    def get_messages(self, token, userid):
        data = self.get('/api/1.0/person/%s/messages/' % userid,
                head={'token': token})
        result = []
        for m in data['messages']:
            result.append(Message(**m))
        return result

    def get_user(self, token, userid):
        data = self.get('/api/1.0/person/%s/' % userid, head={'token': token})
        return Profile(**data['person'])

    def get_profile(self, token):
        data = self.get('/api/1.0/profile/', head={'token': token})
        return Profile(**data['person'])

    def set_profile(self, token, **form):
        data = self.post('/api/1.0/profile/', head={'token': token}, data=form)
        return data['success']
