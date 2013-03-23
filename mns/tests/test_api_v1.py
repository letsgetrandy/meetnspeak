#from django.utils import unittest
from django.test import TestCase
#from django.test.client import Client
#from django.core.urlresolvers import reverse

from mns.api_v1 import MNSAPI
import datetime


class APITests(TestCase):

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    mns = MNSAPI()

    def setUp(self):
        pass

    def signup(self, email, password):
        token = self.mns.signup(email, password)
        return token

    def test_signup(self):
        email = 'test+%s-signup@example.com' % self.timestamp
        password = 'password'
        token = self.mns.signup(email, password)
        assert(token)

    def test_login(self):
        email = 'test+%s-login@example.com' % self.timestamp
        password = 'password'
        token = self.mns.signup(email, password)
        assert(token)
        result = self.mns.login(email, password)
        assert(result)

    def test_contacts(self):
        email = 'test+%s-contacts@example.com' % self.timestamp
        password = 'password'
        token = self.signup(email, password)
        assert(token)
        result = self.mns.get_contacts(token)
        assert(result)

    def test_notifications(self):
        pass

    def test_messages(self):
        pass

    def test_user_page(self):
        pass

    def test_profile(self):
        pass

    def test_settings(self):
        pass
