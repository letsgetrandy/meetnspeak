#from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class FunctionalTests(TestCase):

    def setUp(self):

        pass

    def test_homepage(self):
        client = Client()
        response = client.get(reverse('index'))
        #print response.content

    def test_does_something(self):

        foo = "bar"
        assert(foo == 'bar')

    def test_bar(self):

        assert(1 == 1)
