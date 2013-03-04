from django.utils import unittest


class FooTestCase(unittest.TestCase):

    def setUp(self):

        pass

    def test_does_something(self):

        foo = "bar"
        assert(foo == 'bar')

    def test_bar(self):

        assert(1 == 1)
