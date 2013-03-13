#from django.utils import unittest
from django.test import TestCase
#from django.test.client import Client
#from django.core.urlresolvers import reverse
from mns.api_v1 import MNSAPI


class APITests(TestCase):

    def setUp(self):

        pass

    def test_signup(self):
        mns = MNSAPI()
        token = mns.signup('test@example.com', 'password')
        assert(token)

    def test_does_something(self):

        foo = "bar"
        assert(foo == 'bar')

    def test_bar(self):

        assert(1 == 1)
