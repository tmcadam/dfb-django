from django.test import TestCase
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

    def test_country_sorted_by_name_ascending(self):
        CountryFactory.create(name="Chile")
        CountryFactory.create(name="Argentina")
        CountryFactory.create(name="Brazil")

        self.assertEqual(Country.objects.all().first().name, "Argentina")
        self.assertEqual(Country.objects.all().last().name, "Chile")



