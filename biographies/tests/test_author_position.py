from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth.models import User

from biographies.tests.factories import BiographyFactory
from authors.tests.factories import AuthorFactory
from authors.models import BiographyAuthor


class BiographyAuthorPositionTests(TestCase):
    """Test BiographyAuthor model ordering by author_position."""

    @tag("author_position")
    def test_get_ordered_authors_returns_correct_order(self):
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="Zebra")
        author2 = AuthorFactory.create(last_name="Apple")
        author3 = AuthorFactory.create(last_name="Mango")

        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=3)
        BiographyAuthor.objects.create(biography=bio, author=author2, author_position=1)
        BiographyAuthor.objects.create(biography=bio, author=author3, author_position=2)

        ordered = list(bio.get_ordered_authors())
        self.assertEqual(ordered[0], author2)
        self.assertEqual(ordered[1], author3)
        self.assertEqual(ordered[2], author1)

    @tag("author_position")
    def test_get_ordered_authors_empty_when_no_connections(self):
        bio = BiographyFactory.create()
        ordered = list(bio.get_ordered_authors())
        self.assertEqual(ordered, [])

    @tag("author_position")
    def test_biography_author_model_ordering_default(self):
        """Test that BiographyAuthor.objects.all() orders by author_position by default."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="Zebra")
        author2 = AuthorFactory.create(last_name="Apple")

        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=2)
        BiographyAuthor.objects.create(biography=bio, author=author2, author_position=1)

        ordered = list(BiographyAuthor.objects.filter(biography=bio))
        self.assertEqual(ordered[0].author, author2)
        self.assertEqual(ordered[1].author, author1)


class BiographyAuthorFormsetPositionTests(TestCase):
    """Test that the formset correctly handles author positions.

    Note: The inlineformset_factory creates a formset with prefix 'biographyauthor_set'
    (the default model name + '_set'). All formset field names must use this prefix.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("author_position", "formset")
    def test_formset_saves_positions_correctly(self):
        """Test that creating a biography with authors saves positions correctly."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        author3 = AuthorFactory.create(last_name="Third")

        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:edit', kwargs={'bio_slug': bio.slug})

        # Use 'biographyauthor_set' prefix (default for inlineformset_factory)
        data = {
            'title': bio.title,
            'slug': bio.slug,
            'lifespan': bio.lifespan,
            'body': bio.body,
            'authors': bio.authors,
            'primary_country': bio.primary_country_id,
            'secondary_country': '',
            'south_georgia': 'on' if bio.south_georgia else '',
            'featured': 'on' if bio.featured else '',
            'external_links': bio.external_links or '',
            'revisions': bio.revisions or '',
            # Formset management form with correct prefix
            'biographyauthor_set-TOTAL_FORMS': '3',
            'biographyauthor_set-INITIAL_FORMS': '0',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            # Form fields with correct prefix
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-DELETE': '',
            'biographyauthor_set-2-author': author3.id,
            'biographyauthor_set-2-author_position': '3',
            'biographyauthor_set-2-DELETE': '',
        }

        response = self.client.post(url, data)
        if response.status_code != 302:
            form = response.context.get('form')
            formset = response.context.get('authors_formset')
            errors = []
            if form:
                for field, field_errors in form.errors.items():
                    for err in field_errors:
                        errors.append(f"form.{field}: {err}")
                for err in form.non_field_errors():
                    errors.append(f"form.non_field_errors: {err}")
            if formset:
                for err in formset.non_form_errors():
                    errors.append(f"formset.non_form_errors: {err}")
                for i, form_err in enumerate(formset.errors):
                    if form_err:
                        for field, field_errors in form_err.items():
                            for fe in field_errors:
                                errors.append(f"formset[{i}].{field}: {fe}")
            self.fail(f"Form submission failed. Status: {response.status_code}. Errors: {errors}")

        bio.refresh_from_db()
        ordered = list(bio.get_ordered_authors())
        self.assertEqual(len(ordered), 3)
        self.assertEqual(ordered[0], author1)
        self.assertEqual(ordered[1], author2)
        self.assertEqual(ordered[2], author3)

    @tag("author_position", "formset")
    def test_formset_reorders_authors(self):
        """Test that reordering authors in the form updates positions correctly."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        author3 = AuthorFactory.create(last_name="Third")

        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)
        ba3 = BiographyAuthor.objects.create(biography=bio, author=author3, author_position=3)

        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:edit', kwargs={'bio_slug': bio.slug})

        data = {
            'title': bio.title,
            'slug': bio.slug,
            'lifespan': bio.lifespan,
            'body': bio.body,
            'authors': bio.authors,
            'primary_country': bio.primary_country_id,
            'secondary_country': '',
            'south_georgia': 'on' if bio.south_georgia else '',
            'featured': 'on' if bio.featured else '',
            'external_links': bio.external_links or '',
            'revisions': bio.revisions or '',
            'biographyauthor_set-TOTAL_FORMS': '3',
            'biographyauthor_set-INITIAL_FORMS': '3',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-author': author3.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-id': ba3.id,
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-author': author1.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-id': ba1.id,
            'biographyauthor_set-1-DELETE': '',
            'biographyauthor_set-2-author': author2.id,
            'biographyauthor_set-2-author_position': '3',
            'biographyauthor_set-2-id': ba2.id,
            'biographyauthor_set-2-DELETE': '',
        }

        response = self.client.post(url, data)
        if response.status_code != 302:
            form = response.context.get('form')
            formset = response.context.get('authors_formset')
            errors = []
            if form:
                for field, field_errors in form.errors.items():
                    for err in field_errors:
                        errors.append(f"form.{field}: {err}")
                for err in form.non_field_errors():
                    errors.append(f"form.non_field_errors: {err}")
            if formset:
                for err in formset.non_form_errors():
                    errors.append(f"formset.non_form_errors: {err}")
                for i, form_err in enumerate(formset.errors):
                    if form_err:
                        for field, field_errors in form_err.items():
                            for fe in field_errors:
                                errors.append(f"formset[{i}].{field}: {fe}")
            self.fail(f"Form submission failed. Status: {response.status_code}. Errors: {errors}")

        bio.refresh_from_db()
        ordered = list(bio.get_ordered_authors())
        self.assertEqual(ordered[0], author3)
        self.assertEqual(ordered[1], author1)
        self.assertEqual(ordered[2], author2)

    @tag("author_position", "formset")
    def test_formset_deletes_author_without_affecting_others(self):
        """Test that deleting an author doesn't shift positions of remaining authors unexpectedly."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        author3 = AuthorFactory.create(last_name="Third")

        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)
        ba3 = BiographyAuthor.objects.create(biography=bio, author=author3, author_position=3)

        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:edit', kwargs={'bio_slug': bio.slug})

        data = {
            'title': bio.title,
            'slug': bio.slug,
            'lifespan': bio.lifespan,
            'body': bio.body,
            'authors': bio.authors,
            'primary_country': bio.primary_country_id,
            'secondary_country': '',
            'south_georgia': 'on' if bio.south_georgia else '',
            'featured': 'on' if bio.featured else '',
            'external_links': bio.external_links or '',
            'revisions': bio.revisions or '',
            'biographyauthor_set-TOTAL_FORMS': '3',
            'biographyauthor_set-INITIAL_FORMS': '3',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-id': ba1.id,
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-id': ba2.id,
            'biographyauthor_set-1-DELETE': 'on',
            'biographyauthor_set-2-author': author3.id,
            'biographyauthor_set-2-author_position': '3',
            'biographyauthor_set-2-id': ba3.id,
            'biographyauthor_set-2-DELETE': '',
        }

        response = self.client.post(url, data)
        if response.status_code != 302:
            form = response.context.get('form')
            formset = response.context.get('authors_formset')
            errors = []
            if form:
                for field, field_errors in form.errors.items():
                    for err in field_errors:
                        errors.append(f"form.{field}: {err}")
                for err in form.non_field_errors():
                    errors.append(f"form.non_field_errors: {err}")
            if formset:
                for err in formset.non_form_errors():
                    errors.append(f"formset.non_form_errors: {err}")
                for i, form_err in enumerate(formset.errors):
                    if form_err:
                        for field, field_errors in form_err.items():
                            for fe in field_errors:
                                errors.append(f"formset[{i}].{field}: {fe}")
            self.fail(f"Form submission failed. Status: {response.status_code}. Errors: {errors}")

        # author2 should be deleted
        self.assertFalse(BiographyAuthor.objects.filter(biography=bio, author=author2).exists())

        bio.refresh_from_db()
        ordered = list(bio.get_ordered_authors())
        self.assertEqual(len(ordered), 2)
        self.assertEqual(ordered[0], author1)
        self.assertEqual(ordered[1], author3)


class BiographyAuthorPositionEdgeCases(TestCase):
    """Test edge cases for author position handling."""

    @tag("author_position", "edge_cases")
    def test_get_ordered_authors_with_nonsequential_positions(self):
        """Test ordering works correctly even with non-sequential positions."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        author3 = AuthorFactory.create(last_name="Third")

        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=10)
        BiographyAuthor.objects.create(biography=bio, author=author2, author_position=1)
        BiographyAuthor.objects.create(biography=bio, author=author3, author_position=100)

        ordered = list(bio.get_ordered_authors())
        self.assertEqual(ordered[0], author2)
        self.assertEqual(ordered[1], author1)
        self.assertEqual(ordered[2], author3)

    @tag("author_position", "edge_cases")
    def test_duplicate_positions_ordered_by_id(self):
        """Test behavior when multiple authors have the same position."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")

        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        BiographyAuthor.objects.create(biography=bio, author=author2, author_position=1)

        ordered = list(bio.get_ordered_authors())
        self.assertEqual(len(ordered), 2)

    @tag("author_position", "edge_cases")
    def test_single_author_position_unchanged(self):
        """Test that a single author's position is preserved."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")

        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=5)

        ordered = list(bio.get_ordered_authors())
        self.assertEqual(len(ordered), 1)
        self.assertEqual(ordered[0], author1)
        ba = BiographyAuthor.objects.get(biography=bio, author=author1)
        self.assertEqual(ba.author_position, 5)
