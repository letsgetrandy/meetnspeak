from django.conf import settings
import json
import httplib
import urllib
#import sys


language_name = {
        'EN': 'English',
        'FR': 'French',
        'IT': 'Italian',
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
        self.text = kwargs['text']
        self.target = kwargs['target']
        self.sender = kwargs['sender']
        return


class Contact:

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


class Message:

    def __init__(self, *args, **kwargs):
        self.text = kwargs['text']


class Profile:

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.age = kwargs['age']
        self.hometown = kwargs['hometown']
        self.languages = []
        for lang, lev in kwargs['languages'].items():
            self.languages.append({
                    'name': language_name[lang],
                    'level': language_level[lev],
                })


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
        conn.close
        if st != 200:
            raise APIException(d)
        j = json.loads(d)
        if j.get('token_expired'):
            raise ExpiredToken(j['error'])
        if j.get('bad_login'):
            raise BadLogin(j['error'])
        if not j['success']:
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

    def get_notifications(self, userid):
        data = self.get('/api/1.0/person/%s/notifications/' % userid)
        result = []
        for n in data['notifications']:
            result.append(Notification(**n))
        return result

    def get_contacts(self, userid):
        data = self.get('/api/1.0/person/%s/contacts/' % userid)
        result = []
        for c in data['contacts']:
            result.append(Contact(**c))
        return result

    def get_messages(self, userid):
        data = self.get('/api/1.0/person/%s/messages/' % userid)
        result = []
        for m in data['messages']:
            result.append(Message(**m))
        return result

    def get_profile(self, userid):
        data = self.get('/api/1.0/person/%s/profile/' % userid)
        return Profile(**data['person'])
