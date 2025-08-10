from pathlib import Path
import os

from django.core.files import File

from images.models import Image
from biographies.tests.factories import BiographyFactory

BASE_DIR = Path(__file__).resolve().parent

def create_test_img(image_name, bio=None):
    with open(os.path.join(BASE_DIR,'files', image_name), 'rb') as f:
        img = Image(
            title = "Image Title",
            biography = bio if bio else BiographyFactory.create(),
            caption = "Image Caption",
            attribution = "Image Attribution",
            image = File(f, name=image_name)
        )
        img.full_clean()
        img.save()
        return img
