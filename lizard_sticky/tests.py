from django.contrib.gis.utils import add_srs_entry
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import lizard_sticky.models

from lizard_sticky.models import Sticky
from lizard_sticky.models import Tag

from lizard_map.models import Setting

class ModelTest(TestCase):

    def setUp(self):
        self.client = Client()
        add_srs_entry(900913)  # Add google srs entry.

    def test_smoke(self):
        self.assertTrue(lizard_sticky.models)

    def test_visit_sticky_browser(self):
        url = reverse('lizard_sticky.sticky_browser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_sticky_notags(self):
        """Add sticky without tags.

        x=146414&y=489585.5&reporter=Jack&title=poep
        &description=poep+op+straat&tags=poep
        """

        # X and Y are assumed to be in the site's projection
        # So we need to set one. Should be a fixture.
        s = Setting()
        s.key = 'projection'
        s.value = 'EPSG:28992'
        s.save()

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
