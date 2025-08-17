from django.test import TestCase, tag
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from pages.models import Page


class PageModelTests(TestCase):

    @tag("pages_models")
    def test_can_add_page_with_valid_fields(self):
        page = Page(
            title = "Page Title",
            body = "Page content",
            slug = "joe_blow"
        )
        page.full_clean()
        page.save()
        self.assertEqual(Page.objects.count(), 1)

    @tag("pages_models")
    def test_page_invalid_without_title_field(self):
        with self.assertRaises(ValidationError):
            page = Page(
                title = None,
                body = "some content",
                slug = "joe_blow"
            )
            page.full_clean()
            page.save()

    @tag("pages_models")
    def test_page_invalid_without_body_field(self):
        with self.assertRaises(ValidationError):
            page = Page(
                title = "Some Title",
                body = None,
                slug = "joe_blow"
            )
            page.full_clean()
            page.save()


    @tag("pages_models")
    def test_page_invalid_without_slug_field(self):
        with self.assertRaises(ValidationError):
            page = Page(
                title = "Title",
                body = "some content",
                slug = None
            )
            page.full_clean()
            page.save()


    @tag("pages_models")
    def test_page_invalid_with_bad_slug_field(self):
        with self.assertRaises(ValidationError):
            page = Page(
                title = "Title",
                body = "some content",
                slug = "bad slug"
            )
            page.full_clean()
            page.save()
