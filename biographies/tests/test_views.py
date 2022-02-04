from django.test import TestCase
from django.urls import reverse

from biographies.models import *
from .factories import *

class BiographyViewsTests(TestCase):

    def test_routing_for_show_biography(self):

        BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"]) 
        response = self.client.get(url)
        self.assertContains(response, text="Bio1", status_code=200)