from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from pages.models import Page

class PagesViewsTests(TestCase):

    def test_home_page(self):
        """
        The home view of the DFB site returns a simple test string.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='The Dictionary of Falklands Biography', status_code=200)


    def test_footer_has_admin_link(self):
        """
        The footer contains a link to the admin page.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='/admin/', status_code=200)


    def test_page(self):
        """
        The page view returns a 200 status code.
        """
        Page.objects.create(
            title="Test Page",
            body="This is a test page.",
            slug="test-page"
        )

        url = reverse('pages:show', args=['test-page'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Test Page', status_code=200)
        self.assertContains(response, text='This is a test page.', status_code=200)


    def test_bootstrap_present(self):
        """
        Bootstrap and jquey should be in the page head.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='jquery', status_code=200)
        self.assertContains(response, text='bootstrap', status_code=200)


    def test_page_title(self):
        """
        The title of the page (browser tab) contains the environment name, unless in production.
        """
        url = reverse('pages:home')
        settings.ENVIRONMENT = 'staging'
        response = self.client.get(url)
        self.assertContains(response, text='DFB - Staging', status_code=200)
        settings.ENVIRONMENT = 'production'
        self.assertContains(response, text='DFB', status_code=200)
        self.assertNotContains(response, text='DFB - Production')


    def test_page_has_footer(self):
        """
        The home page contains a footer
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='David Tatham. All rights reserved.', status_code=200)
