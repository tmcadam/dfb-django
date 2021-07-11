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


class BiographyModelTests(TestCase):

    def test_can_create_biography_with_all_fields_present(self):
        BiographyFactory.create(title="Bio1")
        BiographyFactory.create(title="Bio2")
        self.assertEqual(Biography.objects.all().count(), 2)

    def test_create_biography_fails_if_title_missing(self):
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(title=None)

    def test_create_biography_fails_if_title_not_unique(self):
        BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(title="Bio1")

    def test_create_biography_fails_if_slug_missing(self):
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(slug=None)

    def test_create_biography_fails_if_slug_missing(self):
        BiographyFactory.create(slug="jim_bob")
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(slug="jim_bob")

    def test_biograhies_sorted_by_title_ascending(self):
        BiographyFactory.create(title="Clarissa Cunningham")
        BiographyFactory.create(title="Arthur Anderson")
        BiographyFactory.create(title="Belinda Bobby")

        self.assertEqual(Biography.objects.all().first().title, "Arthur Anderson")
        self.assertEqual(Biography.objects.all().last().title, "Clarissa Cunningham")

    def test_create_biography_fails_if_body_missing(self):
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(body=None)

    def test_create_biography_with_primary_and_secondary_country(self):
        c1 = CountryFactory.create()
        c2 = CountryFactory.create()
        BiographyFactory.create(primary_country=c1, secondary_country=c2)
        b1 = Biography.objects.all().first()
        self.assertEqual(b1.primary_country.name, c1.name)
        self.assertEqual(b1.secondary_country.name, c2.name)

    def test_can_create_biography_with_no_primary_country(self):
        BiographyFactory.create(primary_country=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.primary_country)
    
    def test_can_create_biography_with_no_secondary_country(self):
        BiographyFactory.create(secondary_country=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.secondary_country)

    def test_can_create_country_with_south_georgia_set_to_true(self):
        BiographyFactory.create(south_georgia=True)
        b1 = Biography.objects.all().first()
        self.assertTrue(b1.south_georgia)

    def test_can_update_country_to_be_featured(self):
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=False)
        result = Biography.objects.filter(featured=True)
        self.assertEqual(result.count(), 2)