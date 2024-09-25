from django.test import TestCase, tag
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

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

    def test_str_representation_of_country_shows_country_name(self):
        c = CountryFactory.create(name="Chile")
        self.assertEqual(str(c), "Chile")

class BiographyModelTests(TestCase):

    def test_can_create_biography_with_all_fields_present(self):
        BiographyFactory.create(title="Bio1")
        BiographyFactory.create(title="Bio2")
        self.assertEqual(Biography.objects.all().count(), 2)

    def test_create_biography_fails_if_title_missing(self):
        with self.assertRaises(IntegrityError):
            BiographyFactory.create(title=None)

    def test_create_biography_if_title_not_unique(self):
        BiographyFactory.create(title="Bio1")
        BiographyFactory.create(title="Bio1")
        self.assertEqual(Biography.objects.all().count(), 2)

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

    def test_can_create_biography_with_south_georgia_set_to_true(self):
        BiographyFactory.create(south_georgia=True)
        b1 = Biography.objects.all().first()
        self.assertTrue(b1.south_georgia)

    def test_can_update_country_to_be_featured(self):
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=True)
        BiographyFactory.create(featured=False)
        result = Biography.objects.filter(featured=True)
        self.assertEqual(result.count(), 2)

    def test_can_create_biography_with_no_revisions(self):
        BiographyFactory.create(revisions=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.revisions)

    def test_can_create_biography_with_no_authors(self):
        BiographyFactory.create(authors=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.authors)
    
    def test_can_create_biography_with_no_links(self):
        BiographyFactory.create(external_links=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.external_links)
    
    def test_can_create_biography_with_no_references(self):
        BiographyFactory.create(references=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.references)

    def test_can_create_biography_with_no_lifespan(self):
        BiographyFactory.create(lifespan=None)
        b1 = Biography.objects.all().first()
        self.assertIsNone(b1.lifespan)

    def test_str_representation_of_biography_shows_biography_title_and_lifespan(self):
        b = BiographyFactory.create(title="Fred Burns", lifespan="1922-1986")
        self.assertEqual(str(b), "Fred Burns (1922-1986)")
        b = BiographyFactory.create(title="Fred Burns", lifespan=None)
        self.assertEqual(str(b), "Fred Burns")

    def test_bio_save_cleans_urls_in_body(self):
        bio = BiographyFactory(
            body = "before https://www.falklandsbiographies.org/test-url/biographies/12 \
middle https://www.falklandsbiographies.org/test-url/biographies/13 after",
        )
        bio.full_clean()
        bio.save()
        self.assertEqual(bio.body, "before /test-url/biographies/12 middle /test-url/biographies/13 after")


class AuthorModelTests(TestCase):

    # Tests for object creation and validation

    def test_can_create_author_with_all_fields_present(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 1)

    def test_author_without_last_name_is_invalid(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(first_name="Joe", last_name=None, biography="A great author")

    def test_author_without_first_name_is_valid(self):
        Author.objects.create(first_name=None, last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 1)

    def test_author_without_biography_is_valid(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography=None)
        self.assertEqual(Author.objects.all().count(), 1)

    def test_author_with_duplicate_last_name_is_valid_if_first_name_different(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
        Author.objects.create(first_name="Mark", last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 2)

    def test_author_with_duplicate_first_name_and_last_name_is_invalid(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
            Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")

    # Tests for ordering

    def test_authors_are_ordered_by_lastname_and_then_first_name(self):
        Author.objects.create(first_name="Mark", last_name="Black", biography="A great author")
        Author.objects.create(first_name="Simon", last_name="Clifton", biography="A great author")
        Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
        Author.objects.create(first_name="Simon", last_name="Dodds", biography="A great author")
        
        authors_list = Author.objects.all()

        self.assertEqual(authors_list[0].first_name, "Joe")
        self.assertEqual(authors_list[0].last_name, "Black")

        self.assertEqual(authors_list[1].first_name, "Mark")
        self.assertEqual(authors_list[1].last_name, "Black")

        self.assertEqual(authors_list[2].first_name, "Simon")
        self.assertEqual(authors_list[2].last_name, "Clifton")

        self.assertEqual(authors_list[3].first_name, "Simon")
        self.assertEqual(authors_list[3].last_name, "Dodds")

    # Test formatting

    def test_name_joins_first_name_and_last_name_present(self):
        auth = Author.objects.create(first_name="Mark", last_name="Black")
        self.assertEqual(auth.name, "Mark Black")
    
    def test_name_returns_lastname_if_no_first_name_present(self):
        auth = Author.objects.create(first_name=None, last_name="Black")
        self.assertEqual(auth.name, "Black")

    def test_str_joins_first_name_and_last_name_present(self):
        auth = Author.objects.create(first_name="Mark", last_name="Black")
        self.assertEqual(str(auth), "Black, Mark")

    def test_str_returns_lastname_if_no_first_name_present(self):
        auth = Author.objects.create(first_name=None, last_name="Black")
        self.assertEqual(str(auth), "Black")

    def test_simple_slug_cleans_names(self):

        auth1 = Author.objects.create(first_name="Bob", last_name="Author1")
        self.assertEqual(auth1.simple_slug, "bob-author1")

        auth2 = Author.objects.create(first_name="Bob", last_name="Author 1")
        self.assertEqual(auth2.simple_slug, "bob-author-1")

        auth3 = Author.objects.create(first_name="Bob", last_name="Author 1^")
        self.assertEqual(auth3.simple_slug, "bob-author-1")


class BiographyAuthorModelTests(TestCase):

    def test_can_add_author_to_biography_with_valid_fields(self):
        author_1 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

    def test_adding_author_to_biography_fails_without_author_position(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=None)

    def test_adding_author_to_biography_fails_with_duplicate_bio_and_author(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=2)


    def test_adding_author_to_biography_fails_with_duplicate_bio_and_position(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            author_2 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
            BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=1)

    def test_biographyauthor_ordering_by_position(self):
        author_1 = AuthorFactory.create()
        author_2 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=1)
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=2)
        
        biography_authors = BiographyAuthor.objects.filter(biography=bio_1)

        self.assertEqual(biography_authors[0].author, author_2)
        self.assertEqual(biography_authors[1].author, author_1)

    def test_can_add_an_author_directly_to_biography(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        bio_1.authors_connections.add(AuthorFactory.create(), through_defaults={"author_position":1})
        bio_1.authors_connections.add(AuthorFactory.create(), through_defaults={"author_position":2})

        self.assertEqual(bio_1.authors_connections.count(), 2)

    def test_can_access_a_biographies_authors_through_authors_connected_property(self):
        author_1 = AuthorFactory.create()
        author_2 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
        BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=2)

        self.assertEqual(bio_1.authors_connections.count(), 2)

    def test_can_access_an_authors_biographies_through_biographies_property(self):
        author_1 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        bio_2 = BiographyFactory.create(title="Bio2")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
        BiographyAuthor.objects.create(biography=bio_2, author=author_1, author_position=1)

        self.assertEqual(author_1.biographies.count(), 2)

    def test_biographyauthors_destroyed_when_authors_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)
        
        author_1.delete()
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 0)
        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 0)
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 1)

    def test_biographyauthors_destroyed_when_biograhies_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)
        
        bio_1.delete()
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 0)
        self.assertEqual(BiographyAuthor.objects.filter(author=author_1).count(), 0)
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 1)

    def test_biography_and_authors_NOT_destroyed_when_biographyauthor_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        link_1 = BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)

        link_1.delete()
        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 0)
        
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 1)
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 1)


class CommentModelTests(TestCase):


    def test_can_add_comment_to_biography_with_valid_fields(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "Some comment"
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_invalid_without_biography_field(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = None,
                email = "joe@john.com",
                name = "Joe Blow",
                comment = "Some comment"
            )

    def test_comment_invalid_without_email_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = bio_1,
                email = None,
                name = "Joe Blow",
                comment = "Some comment"
            )

    def test_comment_invalid_without_name_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = bio_1,
                email = "joe@blah.com",
                name = None,
                comment = "Some comment"
            )

    def test_comment_invalid_without_comment_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = bio_1,
                email = "joe@blah.com",
                name = "Joe Blow",
                comment = None
            )

    # As this is testing a validator, it should possibly be in form
    # or view tests
    def test_comment_invalid_without_valid_email_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(ValidationError):
            comment = Comment.objects.create(
                biography = bio_1,
                email = "not-a-good-email",
                name = "Joe Blow",
                comment = "Some comment"
            )
            comment.full_clean()

    def test_comment_deleted_when_biography_deleted(self):

        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "Some comment"
        )
        self.assertEqual(Comment.objects.count(), 1)
        bio_1.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_deleted_does_not_delete_biography(self):

        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "Some comment"
        )
        self.assertEqual(Biography.objects.count(), 1)
        comment.delete()
        self.assertEqual(Biography.objects.count(), 1)

    def test_comment_str_method_truncates_comment_field(self):

        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.assertEqual(str(comment), "ABCDEFGHIJKLMNOPQRST...")
