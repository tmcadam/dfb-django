from django.test import TestCase, tag
from django.db.utils import IntegrityError

from biographies.models import Biography
from authors.models import Author, BiographyAuthor
from authors.tests.factories import AuthorFactory
from biographies.tests.factories import BiographyFactory


class AuthorModelTests(TestCase):

    @tag("authors_models")
    def test_can_create_author_with_all_fields_present(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 1)

    @tag("authors_models")
    def test_author_without_last_name_is_invalid(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(first_name="Joe", last_name=None, biography="A great author")

    @tag("authors_models")
    def test_author_without_first_name_is_valid(self):
        Author.objects.create(first_name=None, last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 1)

    @tag("authors_models")
    def test_author_without_biography_is_valid(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography=None)
        self.assertEqual(Author.objects.all().count(), 1)

    @tag("authors_models")
    def test_author_with_duplicate_last_name_is_valid_if_first_name_different(self):
        Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
        Author.objects.create(first_name="Mark", last_name="Black", biography="A great author")
        self.assertEqual(Author.objects.all().count(), 2)

    @tag("authors_models")
    def test_author_with_duplicate_first_name_and_last_name_is_invalid(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")
            Author.objects.create(first_name="Joe", last_name="Black", biography="A great author")

    # Tests for ordering
    @tag("authors_models")
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

    @tag("authors_models")
    def test_name_joins_first_name_and_last_name_present(self):
        auth = Author.objects.create(first_name="Mark", last_name="Black")
        self.assertEqual(auth.name, "Mark Black")
    
    @tag("authors_models")
    def test_name_returns_lastname_if_no_first_name_present(self):
        auth = Author.objects.create(first_name=None, last_name="Black")
        self.assertEqual(auth.name, "Black")

    @tag("authors_models")
    def test_str_joins_first_name_and_last_name_present(self):
        auth = Author.objects.create(first_name="Mark", last_name="Black")
        self.assertEqual(str(auth), "Black, Mark")

    @tag("authors_models")
    def test_str_returns_lastname_if_no_first_name_present(self):
        auth = Author.objects.create(first_name=None, last_name="Black")
        self.assertEqual(str(auth), "Black")

    @tag("authors_models")
    def test_simple_slug_cleans_names(self):

        auth1 = Author.objects.create(first_name="Bob", last_name="Author1")
        self.assertEqual(auth1.simple_slug, "bob-author1")

        auth2 = Author.objects.create(first_name="Bob", last_name="Author 1")
        self.assertEqual(auth2.simple_slug, "bob-author-1")

        auth3 = Author.objects.create(first_name="Bob", last_name="Author 1^")
        self.assertEqual(auth3.simple_slug, "bob-author-1")


class BiographyAuthorModelTests(TestCase):

    @tag("authors_models")
    def test_can_add_author_to_biography_with_valid_fields(self):
        author_1 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

    @tag("authors_models")
    def test_adding_author_to_biography_fails_without_author_position(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=None)

    @tag("authors_models")
    def test_adding_author_to_biography_fails_with_duplicate_bio_and_author(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=2)

    @tag("authors_models")
    def test_adding_author_to_biography_fails_with_duplicate_bio_and_position(self):
        with self.assertRaises(IntegrityError):
            author_1 = AuthorFactory.create()
            author_2 = AuthorFactory.create()
            bio_1 = BiographyFactory.create(title="Bio1")
            BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
            BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=1)

    @tag("authors_models")
    def test_biographyauthor_ordering_by_position(self):
        author_1 = AuthorFactory.create()
        author_2 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=1)
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=2)
        
        biography_authors = BiographyAuthor.objects.filter(biography=bio_1)

        self.assertEqual(biography_authors[0].author, author_2)
        self.assertEqual(biography_authors[1].author, author_1)

    @tag("authors_models")
    def test_can_add_an_author_directly_to_biography(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        bio_1.authors_connections.add(AuthorFactory.create(), through_defaults={"author_position":1})
        bio_1.authors_connections.add(AuthorFactory.create(), through_defaults={"author_position":2})

        self.assertEqual(bio_1.authors_connections.count(), 2)

    @tag("authors_models")
    def test_can_access_a_biographies_authors_through_authors_connected_property(self):
        author_1 = AuthorFactory.create()
        author_2 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
        BiographyAuthor.objects.create(biography=bio_1, author=author_2, author_position=2)

        self.assertEqual(bio_1.authors_connections.count(), 2)

    @tag("authors_models")
    def test_can_access_an_authors_biographies_through_biographies_property(self):
        author_1 = AuthorFactory.create()
        bio_1 = BiographyFactory.create(title="Bio1")
        bio_2 = BiographyFactory.create(title="Bio2")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)
        BiographyAuthor.objects.create(biography=bio_2, author=author_1, author_position=1)

        self.assertEqual(author_1.biographies.count(), 2)

    @tag("authors_models")
    def test_biographyauthors_destroyed_when_authors_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)
        
        author_1.delete()
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 0)
        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 0)
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 1)

    @tag("authors_models")
    def test_biographyauthors_destroyed_when_biograhies_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)
        
        bio_1.delete()
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 0)
        self.assertEqual(BiographyAuthor.objects.filter(author=author_1).count(), 0)
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 1)

    @tag("authors_models")
    def test_biography_and_authors_NOT_destroyed_when_biographyauthor_destroyed(self):
        author_1 = AuthorFactory.create(last_name="Auth1")
        bio_1 = BiographyFactory.create(title="Bio1")
        link_1 = BiographyAuthor.objects.create(biography=bio_1, author=author_1, author_position=1)

        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 1)

        link_1.delete()
        self.assertEqual(BiographyAuthor.objects.filter(biography=bio_1).count(), 0)
        
        self.assertEqual(Biography.objects.filter(title="Bio1").count(), 1)
        self.assertEqual(Author.objects.filter(last_name="Auth1").count(), 1)
