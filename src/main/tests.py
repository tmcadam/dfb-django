from django.test import TestCase
from django.urls import reverse

class MainViewTests(TestCase):

    def test_home_page(self):
        """
        The home view of the DFB site returns a simple
        test string.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, text='DFB HOME', status_code=200)
