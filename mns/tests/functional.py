#from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class FunctionalTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('index'))
        assert(response)

    def test_does_something(self):
        response = self.client.get(reverse('login'))
        assert(response)

    def test_bar(self):
        response = self.client.get(reverse('signup'))
        assert(response)
