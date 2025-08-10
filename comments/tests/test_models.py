from django.test import TestCase, tag
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from comments.models import Comment
from biographies.models import Biography
from biographies.tests.factories import BiographyFactory

class CommentModelTests(TestCase):

    @tag("comments_models")
    def test_can_add_comment_to_biography_with_valid_fields(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "Some comment"
        )
        self.assertEqual(Comment.objects.count(), 1)

    @tag("comments_models")
    def test_comment_invalid_without_biography_field(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = None,
                email = "joe@john.com",
                name = "Joe Blow",
                comment = "Some comment"
            )

    @tag("comments_models")
    def test_comment_invalid_without_email_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = bio_1,
                email = None,
                name = "Joe Blow",
                comment = "Some comment"
            )

    @tag("comments_models")
    def test_comment_invalid_without_name_field(self):
        bio_1 = BiographyFactory.create(title="Bio1")
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                biography = bio_1,
                email = "joe@blah.com",
                name = None,
                comment = "Some comment"
            )

    @tag("comments_models")
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
    @tag("comments_models")
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

    @tag("comments_models")
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

    @tag("comments_models")
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

    @tag("comments_models")
    def test_comment_str_method_truncates_comment_field(self):

        bio_1 = BiographyFactory.create(title="Bio1")
        comment = Comment.objects.create(
            biography = bio_1,
            email = "joe@john.com",
            name = "Joe Blow",
            comment = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.assertEqual(str(comment), "ABCDEFGHIJKLMNOPQRST...")
