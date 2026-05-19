from django.test import TestCase, tag

from biographies.forms import BiographyAuthorForm, BiographyAuthorFormSet
from biographies.models import Biography
from biographies.tests.factories import BiographyFactory
from authors.tests.factories import AuthorFactory
from authors.models import BiographyAuthor


class BiographyAuthorFormTests(TestCase):
    """Test BiographyAuthorForm unit functionality."""

    @tag("forms", "biography_author_form")
    def test_form_init_sets_helper(self):
        """Test that form initialization sets up the crispy helper."""
        bio = BiographyFactory.create()
        form = BiographyAuthorForm(instance=BiographyAuthor.objects.create(
            biography=bio, author=AuthorFactory.create(), author_position=1
        ))
        self.assertIsNotNone(form.helper)
        self.assertFalse(form.helper.form_tag)

    @tag("forms", "biography_author_form")
    def test_form_layout_contains_expected_fields(self):
        """Test that form layout contains id, author (via FieldWithButtons), and author_position fields."""
        from crispy_forms.bootstrap import FieldWithButtons
        form = BiographyAuthorForm()
        layout_fields = list(form.helper.layout.fields)
        self.assertEqual(len(layout_fields), 3)
        self.assertEqual(layout_fields[0], 'id')
        self.assertIsInstance(layout_fields[1], FieldWithButtons)
        self.assertEqual(layout_fields[2], 'author_position')

    @tag("forms", "biography_author_form")
    def test_form_id_in_layout_not_in_fields(self):
        """Test that 'id' is in the layout but not in form.fields (handled by formset)."""
        form = BiographyAuthorForm()
        layout_fields = [str(f) for f in form.helper.layout.fields]
        self.assertIn('id', layout_fields)
        self.assertNotIn('id', form.fields)

    @tag("forms", "biography_author_form")
    def test_form_author_position_field_is_hidden_with_class(self):
        """Test that the author_position field uses a HiddenInput widget with class."""
        form = BiographyAuthorForm()
        from django.forms.widgets import HiddenInput
        self.assertIsInstance(form.fields['author_position'].widget, HiddenInput)
        self.assertEqual(form.fields['author_position'].widget.attrs.get('class'), 'author-position')

    @tag("forms", "biography_author_form")
    def test_form_author_field_has_button_in_layout(self):
        """Test that the author field has a FieldWithButtons widget in the layout."""
        from crispy_forms.bootstrap import FieldWithButtons
        form = BiographyAuthorForm()
        layout_fields = list(form.helper.layout.fields)
        self.assertIsInstance(layout_fields[1], FieldWithButtons)

    @tag("forms", "biography_author_form")
    def test_form_has_correct_meta_fields(self):
        """Test that the form has the correct Meta fields."""
        self.assertEqual(BiographyAuthorForm.Meta.fields, ['id', 'author', 'author_position', 'biography'])

    @tag("forms", "biography_author_form")
    def test_form_has_correct_meta_model(self):
        """Test that the form uses the correct model."""
        self.assertEqual(BiographyAuthorForm.Meta.model, BiographyAuthor)

    @tag("forms", "biography_author_form")
    def test_form_clean_with_author_and_position(self):
        """Test form validation with valid author and position data."""
        bio = BiographyFactory.create()
        author = AuthorFactory.create()
        form = BiographyAuthorForm(data={
            'author': author.id,
            'author_position': '1',
        })
        self.assertTrue(form.is_valid())

    @tag("forms", "biography_author_form")
    def test_form_clean_with_author_only(self):
        """Test form validation with author but no position."""
        author = AuthorFactory.create()
        form = BiographyAuthorForm(data={
            'author': author.id,
            'author_position': '',
        })
        # author_position is required, so this should be invalid
        self.assertFalse(form.is_valid())
        self.assertIn('author_position', form.errors)

    @tag("forms", "biography_author_form")
    def test_form_has_changed_returns_true_when_author_changed(self):
        """Test has_changed returns True when author field changes."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        ba = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)

        form = BiographyAuthorForm(
            instance=ba,
            data={'author': author2.id, 'author_position': '1'}
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.has_changed())

    @tag("forms", "biography_author_form")
    def test_form_has_changed_returns_false_when_nothing_changed(self):
        """Test has_changed returns False when nothing changes."""
        bio = BiographyFactory.create()
        author = AuthorFactory.create(last_name="First")
        ba = BiographyAuthor.objects.create(biography=bio, author=author, author_position=1)

        form = BiographyAuthorForm(
            instance=ba,
            data={'author': author.id, 'author_position': '1'}
        )
        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_changed())

    @tag("forms", "biography_author_form")
    def test_form_has_changed_true_when_only_position_changed(self):
        """Test has_changed returns True when only position changes (author also considered changed).

        When author_position changes but author is not in data, the form considers
        both author and author_position as changed (author from instance value to empty).
        The has_changed method only returns False when author_position is the ONLY changed field
        AND author is not provided in data.
        """
        bio = BiographyFactory.create()
        author = AuthorFactory.create(last_name="First")
        ba = BiographyAuthor.objects.create(biography=bio, author=author, author_position=1)

        # When author_position changes and author is not in data,
        # both fields are considered changed, so has_changed returns True
        form = BiographyAuthorForm(
            instance=ba,
            data={'author_position': '2'}  # No author field
        )
        # author_position changed, and author is also considered changed (from instance to empty)
        self.assertTrue(form.has_changed())

    @tag("forms", "biography_author_form")
    def test_form_has_changed_true_when_position_changed_with_empty_author(self):
        """Test has_changed returns True when position changes and author is empty string.

        When author is explicitly empty string in data, the form considers both
        author and author_position as changed.
        """
        bio = BiographyFactory.create()
        author = AuthorFactory.create(last_name="First")
        ba = BiographyAuthor.objects.create(biography=bio, author=author, author_position=1)

        form = BiographyAuthorForm(
            instance=ba,
            data={'author': '', 'author_position': '5'}
        )
        # Both author (from instance to empty) and author_position changed
        self.assertTrue(form.has_changed())


class BiographyAuthorFormSetTests(TestCase):
    """Test BiographyAuthorFormSet functionality."""

    @tag("forms", "formset")
    def test_formset_uses_biography_author_form(self):
        """Test that the formset uses BiographyAuthorForm as its form class."""
        bio = BiographyFactory.create()
        formset = BiographyAuthorFormSet(instance=bio)
        # The formset.form is the form class used by the formset
        self.assertEqual(formset.form.__name__, 'BiographyAuthorForm')

    @tag("forms", "formset")
    def test_formset_extra_forms_zero(self):
        """Test that the formset has extra=0 (no empty forms by default)."""
        bio = BiographyFactory.create()
        formset = BiographyAuthorFormSet(instance=bio)
        # With no existing BiographyAuthor instances, extra=0 means no forms
        self.assertEqual(len(formset.forms), 0)

    @tag("forms", "formset")
    def test_formset_with_existing_instances(self):
        """Test that the formset creates forms for existing instances."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)

        formset = BiographyAuthorFormSet(instance=bio)
        self.assertEqual(len(formset.forms), 2)

    @tag("forms", "formset")
    def test_formset_management_form(self):
        """Test that the formset management form has correct values."""
        bio = BiographyFactory.create()
        formset = BiographyAuthorFormSet(instance=bio)
        # initial_form_count and total_form_count are methods on the formset
        self.assertEqual(formset.initial_form_count(), 0)
        self.assertEqual(formset.total_form_count(), 0)

    @tag("forms", "formset")
    def test_formset_with_instances_management_form(self):
        """Test management form counts with existing instances."""
        bio = BiographyFactory.create()
        author = AuthorFactory.create()
        BiographyAuthor.objects.create(biography=bio, author=author, author_position=1)

        formset = BiographyAuthorFormSet(instance=bio)
        self.assertEqual(formset.initial_form_count(), 1)
        self.assertEqual(formset.total_form_count(), 1)

    @tag("forms", "formset")
    def test_formset_can_delete_is_true(self):
        """Test that the formset allows deletion (can_delete=True)."""
        bio = BiographyFactory.create()
        formset = BiographyAuthorFormSet(instance=bio)
        self.assertTrue(formset.can_delete)

    @tag("forms", "formset")
    def test_formset_validates_correctly(self):
        """Test formset validation with valid data."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)

        data = {
            'biographyauthor_set-TOTAL_FORMS': '2',
            'biographyauthor_set-INITIAL_FORMS': '2',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-id': ba1.id,
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-id': ba2.id,
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-DELETE': '',
        }

        formset = BiographyAuthorFormSet(data)
        self.assertTrue(formset.is_valid())

    @tag("forms", "formset")
    def test_formset_saves_correctly(self):
        """Test that saving a valid formset persists changes."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)

        data = {
            'biographyauthor_set-TOTAL_FORMS': '2',
            'biographyauthor_set-INITIAL_FORMS': '2',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-id': ba1.id,
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-id': ba2.id,
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '3',
            'biographyauthor_set-1-DELETE': '',
        }

        formset = BiographyAuthorFormSet(data, instance=bio)
        self.assertTrue(formset.is_valid())
        saved_instances = formset.save()

        # Verify the position was updated
        ba2.refresh_from_db()
        self.assertEqual(ba2.author_position, 3)

    @tag("forms", "formset")
    def test_formset_deletes_marked_instances(self):
        """Test that deleting marked forms removes instances."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)

        data = {
            'biographyauthor_set-TOTAL_FORMS': '2',
            'biographyauthor_set-INITIAL_FORMS': '2',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-id': ba1.id,
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-id': ba2.id,
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-DELETE': 'on',
        }

        formset = BiographyAuthorFormSet(data, instance=bio)
        self.assertTrue(formset.is_valid())
        formset.save()

        # Verify ba2 was deleted
        self.assertFalse(BiographyAuthor.objects.filter(id=ba2.id).exists())
        # Verify ba1 still exists
        self.assertTrue(BiographyAuthor.objects.filter(id=ba1.id).exists())

    @tag("forms", "formset")
    def test_formset_adds_new_instance(self):
        """Test that adding a new form to the formset creates a new instance."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)

        data = {
            'biographyauthor_set-TOTAL_FORMS': '2',
            'biographyauthor_set-INITIAL_FORMS': '1',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-id': ba1.id,
            'biographyauthor_set-0-author': author1.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-author': author2.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-DELETE': '',
        }

        formset = BiographyAuthorFormSet(data, instance=bio)
        self.assertTrue(formset.is_valid())
        saved_instances = formset.save()

        # Verify new BiographyAuthor was created
        self.assertEqual(BiographyAuthor.objects.filter(biography=bio).count(), 2)

    @tag("forms", "formset")
    def test_formset_reorders_instances(self):
        """Test that reordering authors in the formset updates positions."""
        bio = BiographyFactory.create()
        author1 = AuthorFactory.create(last_name="First")
        author2 = AuthorFactory.create(last_name="Second")
        author3 = AuthorFactory.create(last_name="Third")
        ba1 = BiographyAuthor.objects.create(biography=bio, author=author1, author_position=1)
        ba2 = BiographyAuthor.objects.create(biography=bio, author=author2, author_position=2)
        ba3 = BiographyAuthor.objects.create(biography=bio, author=author3, author_position=3)

        # Reorder: author3 -> 1, author1 -> 2, author2 -> 3
        data = {
            'biographyauthor_set-TOTAL_FORMS': '3',
            'biographyauthor_set-INITIAL_FORMS': '3',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
            'biographyauthor_set-0-id': ba3.id,
            'biographyauthor_set-0-author': author3.id,
            'biographyauthor_set-0-author_position': '1',
            'biographyauthor_set-0-DELETE': '',
            'biographyauthor_set-1-id': ba1.id,
            'biographyauthor_set-1-author': author1.id,
            'biographyauthor_set-1-author_position': '2',
            'biographyauthor_set-1-DELETE': '',
            'biographyauthor_set-2-id': ba2.id,
            'biographyauthor_set-2-author': author2.id,
            'biographyauthor_set-2-author_position': '3',
            'biographyauthor_set-2-DELETE': '',
        }

        formset = BiographyAuthorFormSet(data, instance=bio)
        self.assertTrue(formset.is_valid())
        formset.save()

        # Verify positions were updated
        ba1.refresh_from_db()
        ba2.refresh_from_db()
        ba3.refresh_from_db()
        self.assertEqual(ba1.author_position, 2)
        self.assertEqual(ba2.author_position, 3)
        self.assertEqual(ba3.author_position, 1)
