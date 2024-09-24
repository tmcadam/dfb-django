import os
from pathlib import Path
import shutil
import tempfile

from django.test import TestCase, tag, override_settings
from django.core.files import File

from dfb import settings
from images.models import *
from biographies.models import *
from biographies.tests.factories import *

BASE_DIR = Path(__file__).resolve().parent

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ImageModelTests(TestCase):

    def setup_method(self, test_method):
        self.images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        if os.path.exists(self.images_dir):
            shutil.rmtree(self.images_dir)
        os.mkdir(self.images_dir)

    @tag("current")
    def test_create_image(self):
        
        img = Image.objects.create(
            title = "Image Title",
            biography = BiographyFactory.create(),
            caption = "Image Caption",
            attribution = "Image Attribution"
        )
        img.image.save(
            'test_image_1.jpg',
            File(open(os.path.join(BASE_DIR,'files','test_image_1.jpg'), 'rb'))
        )

        self.assertEqual(Image.objects.count(), 1)

        self.assertTrue(os.path.exists(img.image.path))
        self.assertEqual(img.image.height, 731)
        self.assertEqual(img.image.width, 800)

        self.assertTrue(os.path.exists(img.image300x300.path))
        self.assertEqual(img.image300x300.height, 274)
        self.assertEqual(img.image300x300.width, 300)

        self.assertTrue(os.path.exists(img.image100x100.path))
        self.assertEqual(img.image100x100.height, 91)
        self.assertEqual(img.image100x100.width, 100)