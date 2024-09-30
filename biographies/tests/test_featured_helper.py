import tempfile

from django.test import TestCase, tag, override_settings
from django.db.models.query import QuerySet

from biographies.models import *
from images.models import Image
from images.tests.utils import create_test_img
from biographies.featured_helper import *
from .factories import *

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class BiographyModelTests(TestCase):

    @tag("featured_helper")
    def test_can_set_queryset_to_featured(self):
        bio1 = BiographyFactory.create(featured=False)
        bio2 = BiographyFactory.create(featured=False)
        
        bios = Biography.objects.all()
        set_featured(bios)
        self.assertEqual(Biography.objects.filter(featured=True).count(), 2)

    @tag("featured_helper")
    def test_can_clear_all_featured(self):
        bio1 = BiographyFactory.create(featured=True)
        bio2 = BiographyFactory.create(featured=True)
        
        self.assertEqual(Biography.objects.filter(featured=True).count(), 2)
        clear_featured()
        self.assertEqual(Biography.objects.filter(featured=False).count(), 2)

    @tag("featured_helper")
    def test_can_filter_to_biographies_with_images(self):
        bio1 = BiographyFactory.create(title="Bio1")
        bio2 = BiographyFactory.create(title="Bio2")
        img1 = Image.objects.create(
            title = "Image Title1",
            biography = bio1,
            caption = "Image Caption",
            attribution = "Image Attribution",
            image = "some_image_path"
        )
        bios = Biography.objects.all()
        bios = with_images(bios)
        self.assertEqual(bios.count(), 1)
        self.assertEqual(bios.first().title, "Bio1")

    @tag("featured_helper")
    def test_can_filter_to_biographies_with_lifespan_and_authors(self):
        bio1 = BiographyFactory.create(title="Bio1")
        bio2 = BiographyFactory.create(title="Bio2")
        bio3 = BiographyFactory.create(title="Bio3")

        bio1.lifespan = None
        bio1.full_clean()
        bio1.save()

        bio2.authors = None
        bio2.full_clean()
        bio2.save()

        bio3.full_clean()
        bio3.save()
        bios = Biography.objects.all()
        self.assertEqual(bios.count(), 3)
        bios = with_lifespan_author(bios)
        self.assertEqual(bios.count(), 1)
        self.assertEqual(bios.first().title, "Bio3")

    @tag("featured_helper")
    def test_can_filter_to_biographies_with_first_image_orienatation(self):
        bio1 = BiographyFactory.create(title="Bio1")
        bio2 = BiographyFactory.create(title="Bio2")

        img1 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img2 = create_test_img('test_image_4.jpg', bio=bio1) #portrait
        img3 = create_test_img('test_image_4.jpg', bio=bio2) #portrait
        
        bios = Biography.objects.all()
        self.assertEqual(bios.count(), 2)
        bios = with_first_image_orientated(bios, "portrait")
        self.assertEqual(len(bios), 1)
        self.assertEqual(bios[0].title, "Bio2")

    @tag("featured_helper")
    def test_can_get_random_bios_from_list(self):
        bio1 = BiographyFactory.create(title="Bio1")
        bio2 = BiographyFactory.create(title="Bio2")
        bio3 = BiographyFactory.create(title="Bio3")

        bios = Biography.objects.all()
        self.assertEqual(bios.count(), 3)

        bios_list = get_random_from_list(list(bios), 2)
        self.assertEqual(len(bios_list), 2)


    @tag("featured_helper")
    def test_can_get_queryset_from_list(self):
        bio1 = BiographyFactory.create(title="Bio1")
        bio2 = BiographyFactory.create(title="Bio2")
        bio3 = BiographyFactory.create(title="Bio3")

        bios = list(Biography.objects.all())
        self.assertEqual(type(bios), list)
        self.assertEqual(len(bios), 3)
        bios = get_queryset_from_list(bios)
        self.assertEqual(type(bios), QuerySet)
        self.assertEqual(bios.count(), 3)

