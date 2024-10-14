import tempfile
from datetime import datetime as dt, timedelta as td, timezone as tz

from django.test import TestCase, tag, override_settings
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from biographies.models import Biography, Country
from biographies.tests.factories import BiographyFactory, CountryFactory
from authors.tests.factories import AuthorFactory
from images.tests.utils import create_test_img

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

    def test_str_representation_of_country_shows_country_name(self):
        c = CountryFactory.create(name="Chile")
        self.assertEqual(str(c), "Chile")

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class BiographyModelTests(TestCase):

    @tag("biographies")
    def test_can_create_biography_with_all_fields_present(self):
        bio = BiographyFactory()
        bio.full_clean()
        bio.save()
        self.assertEqual(Biography.objects.all().count(), 1)

    @tag("biographies")
    def test_create_biography_fails_if_title_missing(self):
        with self.assertRaises(ValidationError):
            bio = BiographyFactory()
            bio.title = None
            bio.full_clean()
            bio.save()

    @tag("biographies")
    def test_create_biography_if_title_not_unique(self):
        bio1 = BiographyFactory(title="Bio1")
        bio1.full_clean()
        bio1.save()
        bio2 = BiographyFactory(title="Bio1")
        bio2.full_clean()
        bio2.save()
        self.assertEqual(Biography.objects.all().count(), 2)

    @tag("biographies")
    def test_create_biography_fails_if_slug_missing(self):
        with self.assertRaises(ValidationError):
            bio = BiographyFactory()
            bio.slug = None
            bio.full_clean()
            bio.save()

    @tag("biographies")
    def test_create_biography_fails_if_body_missing(self):
        with self.assertRaises(ValidationError):
            bio = BiographyFactory()
            bio.body = None
            bio.full_clean()
            bio.save()

    @tag("biographies")
    def test_biograhies_sorted_by_title_ascending(self):
        BiographyFactory.create(title="Clarissa Cunningham")
        BiographyFactory.create(title="Arthur Anderson")
        BiographyFactory.create(title="Belinda Bobby")

        self.assertEqual(Biography.objects.all().first().title, "Arthur Anderson")
        self.assertEqual(Biography.objects.all().last().title, "Clarissa Cunningham")

    @tag("biographies")
    def test_create_biography_with_primary_and_secondary_country(self):
        c1 = CountryFactory.create()
        c2 = CountryFactory.create()
        bio = BiographyFactory(primary_country=c1, secondary_country=c2)
        bio.full_clean()
        bio.save()

        b1 = Biography.objects.all().first()
        self.assertEqual(b1.primary_country.name, c1.name)
        self.assertEqual(b1.secondary_country.name, c2.name)

    @tag("biographies")
    def test_can_create_biography_with_no_primary_country(self):
        bio = BiographyFactory()
        bio.primary_country = None
        bio.full_clean()
        bio.save()

        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.primary_country)
    
    @tag("biographies")
    def test_can_create_biography_with_no_secondary_country(self):
        bio = BiographyFactory()
        bio.secondary_country = None
        bio.full_clean()
        bio.save()
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.secondary_country)

    @tag("biographies")
    def test_biography_revisions_have_white_space_cleaned_in_save(self):
        bio = BiographyFactory()
        bio.revisions = " "        
        bio.full_clean()
        bio.save()
        b1 = Biography.objects.all().first()
        self.assertEqual(b1.revisions, "")

    @tag("biographies")
    def test_biography_references_have_white_space_cleaned_in_save(self):
        bio = BiographyFactory()
        bio.references = " "        
        bio.full_clean()
        bio.save()
        b1 = Biography.objects.all().first()
        self.assertEqual(b1.references, "")

    @tag("biographies")
    def test_external_links_have_white_space_cleaned_in_save(self):
        bio = BiographyFactory()
        bio.external_links = " "        
        bio.full_clean()
        bio.save()
        b1 = Biography.objects.all().first()
        self.assertEqual(b1.external_links, "")

    @tag("biographies")
    def test_authors_have_white_space_cleaned_in_save(self):
        bio = BiographyFactory()
        bio.authors = " "        
        bio.full_clean()
        bio.save()
        b1 = Biography.objects.all().first()
        self.assertEqual(b1.authors, "")

    @tag("biographies")
    def test_can_create_biography_with_south_georgia_set_to_true(self):
        bio = BiographyFactory()
        bio.south_georgia=True
        bio.full_clean()
        bio.save()

        b1 = Biography.objects.all().first()
        self.assertTrue(b1.south_georgia)

    @tag("biographies")
    def test_can_update_country_to_be_featured(self):
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=False)
        result = Biography.objects.filter(featured=True)
        self.assertEqual(result.count(), 2)
    
    @tag("biographies")
    def test_can_create_biography_with_no_revisions(self):
        bio = BiographyFactory.create()
        bio.revisions=None
        bio.full_clean()
        bio.save()

        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.revisions)

    @tag("biographies")
    def test_can_create_biography_with_no_authors(self):
        bio = BiographyFactory.create()
        bio.authors=None
        bio.full_clean()
        bio.save()
        
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.authors)
    
    @tag("biographies")    
    def test_can_create_biography_with_no_links(self):
        bio = BiographyFactory.create()
        bio.external_links=None
        bio.full_clean()
        bio.save()
        
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.external_links)

    @tag("biographies")    
    def test_can_create_biography_with_no_references(self):
        bio = BiographyFactory.create()
        bio.references=None
        bio.full_clean()
        bio.save()
        
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.references)

    @tag("biographies")
    def test_can_create_biography_with_no_lifespan(self):
        bio = BiographyFactory.create()
        bio.lifespan=None
        bio.full_clean()
        bio.save()
        
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.lifespan)

    @tag("biographies")
    def test_str_representation_of_biography_shows_biography_title_and_lifespan(self):
        b = BiographyFactory(title="Fred Burns", lifespan="1922-1986")
        b.full_clean()
        b.save()
        self.assertEqual(str(b), "Fred Burns (1922-1986)")
        b = BiographyFactory(title="Fred Burns", lifespan=None)
        b.full_clean()
        b.save()
        self.assertEqual(str(b), "Fred Burns")

    @tag("biographies")
    def test_bio_save_cleans_urls_in_body(self):
        bio = BiographyFactory(
            body = "<p>before <a href=\"https://www.falklandsbiographies.org/biographies/some-bio\">after</a></p>",
        )
        bio.full_clean()
        bio.save()
        self.assertEqual(bio.body, "<p>before <a href=\"/biographies/some-bio\">after</a></p>")


    @tag("biographies")
    def test_can_get_url_of_first_image_medium_size(self):

        bio1 = BiographyFactory.create(title="Bio1")
        img1 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img2 = create_test_img('test_image_4.jpg', bio=bio1) #portrait
        
        self.assertEqual(bio1.featured_image_url, img1.image300x300.url)


    @tag("biographies")
    def test_get_ordered_authors_is_ordering_by_author_position_in_biographyauthor(self):

        author_1 = AuthorFactory.create()
        author_2 = AuthorFactory.create()
        author_3 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        bio_1.authors_connections.add(author_1, through_defaults={"author_position":2})
        bio_1.authors_connections.add(author_3, through_defaults={"author_position":3})
        bio_1.authors_connections.add(author_2, through_defaults={"author_position":1})

        ordered_authors = bio_1.get_ordered_authors()

        self.assertEqual(ordered_authors[0], author_2)
        self.assertEqual(ordered_authors[1], author_1)
        self.assertEqual(ordered_authors[2], author_3)

    @tag("biographies")
    def test_approved_comments_filters_and_orders_comments_for_display(self):
        
        bio1 = BiographyFactory.create(title="Bio1")
        comment1 = bio1.comments.create(name="Joe", email="joe@blah.com", comment="Comment 1")
        comment2 = bio1.comments.create(name="Tom", email="tom@blah.com", comment="Comment 2")
        comment3 = bio1.comments.create(name="Sam", email="sam@blah.com", comment="Comment 3")

        comment1.approved=True
        comment3.created_at = dt.now(tz.utc) - td(days=3)
        comment1.save()
        comment3.approved=True
        comment3.created_at = dt.now(tz.utc) - td(days=7)
        comment3.save()

        self.assertEqual(bio1.comments.all().count(), 3)
        self.assertEqual(bio1.approved_comments().count(), 2)
        # Sam's comment is older so should be displayed first
        self.assertEqual(bio1.approved_comments()[0].name, "Sam")
        self.assertEqual(bio1.approved_comments()[1].name, "Joe")

