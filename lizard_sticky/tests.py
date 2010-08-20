from django.test import TestCase

import lizard_sticky.models


class ModelTest(TestCase):

    def test_smoke(self):
        self.assertTrue(lizard_sticky.models)
