from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.db.utils import IntegrityError

from biographies.models import *
from .factories import *

class CountryModelTests(TestCase):

    def test_create_country(self):
        CountryFactory.create(name="Northern Ireland")
        CountryFactory.create(name="Scotland")
        self.assertEqual(Country.objects.all().count(), 2)

    def test_create_country_fails_if_name_missing(self):
        with self.assertRaises(IntegrityError):
            CountryFactory.create(name=None)

    def test_create_country_fails_if_not_unique(self):
        CountryFactory.create(name="Northern Ireland")
        with self.assertRaises(IntegrityError):
            CountryFactory.create(name="Northern Ireland")


class BiographiesViewsTests(TestCase):

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