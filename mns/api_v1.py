from django.conf import settings
import json
import httplib
import urllib
#import sys


class Notification(object):

    text = ''
    target = 0
    sender = 0

    def __init__(self, *args, **kwargs):
        self.text = kwargs['text']
        self.target = kwargs['target']
        self.sender = kwargs['sender']
        return


class Contact(object):

    id = 0
    name = ''

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


class Profile(object):

    id = 0
    name = ''
    age = 0
    hometown = ''

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.age = kwargs['age']
        self.hometown = kwargs['hometown']


class APIException(Exception):
    pass


class ExpiredToken(Exception):
    pass


class BadLogin(Exception):
    pass


class APIBase(object):
    def request(self, endpoint, method='GET', data=None):
        headers = {
                'Accept': 'text/json',
            }
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

    def get(self, endpoint, data=None):
        return self.request(endpoint, data=data)

    def post(self, endpoint, data=None):
        return self.request(endpoint, method='POST', data=data)


class MNSAPI(APIBase):

    def get_notifications(self, userid):
        data = self.get('/api/v1/person/%s/notifications/' % userid)
        result = []
        for n in data['notifications']:
            result.append(Notification(**n))
        return result

    def get_contacts(self, userid):
        data = self.get('/api/v1/person/%s/contacts/' % userid)
        result = []
        for c in data['contacts']:
            result.append(Contact(**c))
        return result

    def get_profile(self, userid):
        data = self.get('/api/v1/person/%s/profile/' % userid)
        return Profile(**data['person'])
