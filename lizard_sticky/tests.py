from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import lizard_sticky.models

from lizard_sticky.models import Sticky
from lizard_sticky.models import Tag
from lizard_sticky.views import add_sticky


class ModelTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_smoke(self):
        self.assertTrue(lizard_sticky.models)

    def test_create_sticky_notags(self):
        url = reverse('lizard_sticky.add_sticky')
        self.client.post(
            url, {'reporter': 'Jack',
                  'title': 'test geeltje',
                  'description': 'beschrijving test geeltje',
                  'x': '100.0',
                  'y': '100.0',
                  'tags': ''})
        sticky = Sticky.objects.get(reporter='Jack')
        self.assertTrue(sticky)
        self.assertTrue(str(sticky))

    def test_create_sticky_tags(self):
        url = reverse('lizard_sticky.add_sticky')
        self.client.post(
            url, {'reporter': 'Jack',
                  'title': 'nog een test geeltje',
                  'description': 'beschrijving test geeltje',
                  'x': '100.0',
                  'y': '100.0',
                  'tags': 'dit zijn losse tags'})
        self.assertTrue(Tag.objects.get(slug='dit'))
        self.assertTrue(Tag.objects.get(slug='zijn'))
        self.assertTrue(Tag.objects.get(slug='losse'))
        self.assertTrue(Tag.objects.get(slug='tags'))
        self.assertTrue(str(Tag.objects.get(slug='tags')))
