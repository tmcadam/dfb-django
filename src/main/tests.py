from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import os


class MainViewTests(TestCase):

    def test_home_page(self):
        """
        The home view of the DFB site returns a simple
        test string.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, text='DFB HOME', status_code=200)


    def test_bootstrap_present(self):
        """
        Bootstrap and jquey should be in the page head.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, text='jquery', status_code=200)
        self.assertContains(response, text='bootstrap', status_code=200)


    def test_page_title(self):
        """
        The title of the page (browser tab) contains the environment name, 
        unless in production.
        """
        url = reverse('home')
        settings.ENVIRONMENT = 'staging'
        response = self.client.get(url)
        self.assertContains(response, text='DFB - Staging', status_code=200)
        settings.ENVIRONMENT = 'production'
        self.assertContains(response, text='DFB', status_code=200)
        self.assertNotContains(response, text='DFB - Production')