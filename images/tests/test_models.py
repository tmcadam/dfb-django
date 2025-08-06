import os
import tempfile

from django.test import TestCase, tag, override_settings
from django.core.files import File
from django.core.exceptions import ValidationError

from django.conf import settings
from images.models import Image
from biographies.tests.factories import BiographyFactory

from .utils import create_test_img

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ImageModelTests(TestCase):

    @tag("images")
    def test_create_image_with_all_fields(self):

        img = Image(
            title = "Image Title",
            biography = BiographyFactory.create(),
            caption = "Image Caption",
            attribution = "Image Attribution",
            image = "some_image_path"
        )
        img.full_clean()
        img.save()
        self.assertEqual(Image.objects.count(), 1)

    @tag("images")
    def test_field_alias_works_as_expected(self):

        img = create_test_img('test_image_1.jpg')

        self.assertEqual(img.image.url, img.original.url)
        self.assertEqual(img.image300x300.url, img.medium.url)
        self.assertEqual(img.image100x100.url, img.thumbnail.url)

    @tag("images")
    def test_create_image_fails_without_title(self):

        with self.assertRaises(ValidationError):
            img = Image(
                title = None,
                biography = BiographyFactory.create(),
                caption = "Image Caption",
                attribution = "Image Attribution",
                image = "some_image_path"
            )
            img.full_clean()
            img.save()

    @tag("images")
    def test_create_image_fails_without_image(self):

        with self.assertRaises(ValidationError):
            img = Image(
                title = "Title",
                biography = BiographyFactory.create(),
                caption = "Image Caption",
                attribution = "Image Attribution",
                image=None
            )
            img.full_clean()
            img.save()

    @tag("images")
    def test_create_image_fails_without_caption(self):

        with self.assertRaises(ValidationError):
            img = Image(
                title = "title",
                biography = BiographyFactory.create(),
                caption = None,
                attribution = "Image Attribution",
                image = "some_image_path"
            )
            img.full_clean()
            img.save()

    @tag("images")
    def test_create_image_fails_without_biography(self):

        with self.assertRaises(ValidationError):
            img = Image(
                title = "title",
                biography = None,
                caption = "Image caption",
                attribution = "Image Attribution",
                image = "some_image_path"
            )
            img.full_clean()
            img.save()

    @tag("images")
    def test_create_image_okay_without_attribution(self):

        img = Image(
            title = "title",
            biography = BiographyFactory.create(),
            caption = "Image caption",
            attribution = None,
            image = "some_image_path"
        )
        img.full_clean()
        img.save()
        self.assertEqual(Image.objects.count(), 1)

    @tag("images")
    def test_create_image_with_jpeg(self):

        img = create_test_img('test_image_1.jpg')
        self.assertEqual(Image.objects.count(), 1)
        self.assertTrue(os.path.exists(img.image.path))
        self.assertTrue(os.path.exists(img.image300x300.path))
        self.assertTrue(os.path.exists(img.image100x100.path))

    @tag("images")
    def test_create_image_with_tif(self):

        img = create_test_img('test_image_2.tif')
        self.assertTrue(os.path.exists(img.image.path))
        self.assertTrue(os.path.exists(img.image300x300.path))
        self.assertTrue(os.path.exists(img.image100x100.path))

    @tag("images")
    def test_create_image_with_png(self):

        img = create_test_img('test_image_3.png')
        self.assertTrue(os.path.exists(img.image.path))
        self.assertTrue(os.path.exists(img.image300x300.path))
        self.assertTrue(os.path.exists(img.image100x100.path))

    @tag("images")
    def test_large_images_downsized_correctly(self):

        img = create_test_img('test_image_1.jpg')

        self.assertEqual(img.image.height, 731)
        self.assertEqual(img.image.width, 800)

        self.assertEqual(img.image300x300.height, 274)
        self.assertEqual(img.image300x300.width, 300)

        self.assertEqual(img.image100x100.height, 91)
        self.assertEqual(img.image100x100.width, 100)

    @tag("images")
    def test_small_images_not_resized(self):

        img = create_test_img('test_image_3.png')

        self.assertEqual(img.image.height, 86)
        self.assertEqual(img.image.width, 100)

        self.assertEqual(img.image300x300.height, 86)
        self.assertEqual(img.image300x300.width, 100)

        self.assertEqual(img.image100x100.height, 86)
        self.assertEqual(img.image100x100.width, 100)

    @tag("images")
    def test_image_orientation(self):
        img1 = create_test_img('test_image_1.jpg')
        self.assertEqual(img1.orientation, "square")

        img2 = create_test_img('test_image_2.tif')
        self.assertEqual(img2.orientation, "landscape")

        img4 = create_test_img('test_image_4.jpg')
        self.assertEqual(img4.orientation, "portrait")

    @tag("images")
    def test_img_save_cleans_urls_from_caption(self):
        BiographyFactory.create(slug="some-bio")
        img = Image(
            title = "Image Title",
            biography = BiographyFactory.create(),
            caption = """<p>before <a href="https://www.falklandsbiographies.org/biographies/some-bio">after</a></p>""",
            attribution = "Image Attribution",
            image = "some_image_path"
        )
        img.full_clean()
        img.save()
        self.assertEqual(img.caption, """<p>before <a href="/biographies/some-bio">after</a></p>""")

    @tag("images")
    def test_can_get_images_from_biography(self):
        bio1 = BiographyFactory()
        img1 = Image.objects.create(
            title = "Image Title1",
            biography = bio1,
            caption = "Image Caption",
            attribution = "Image Attribution",
            image = "some_image_path"
        )
        img2 = Image.objects.create(
            title = "Image Title2",
            biography = bio1,
            caption = "Image Caption",
            attribution = "Image Attribution",
            image = "some_image_path"
        )
        self.assertEqual(bio1.images.count(), 2)

