import tempfile

from bs4 import BeautifulSoup
from django.test import TestCase, tag, override_settings

from biographies.tests.factories import BiographyFactory
from biographies.tests.sample_body import sample_body_1
from biographies.images_helper import get_body_elements, \
                                        generate_image_tags, insert_image
from images.tests.utils import create_test_img

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ImagesHelperTests(TestCase):

    @tag("images_helper")
    def test_get_body_elements_returns_elements(self):
        elements = get_body_elements(sample_body_1)
        self.assertEqual(len(elements), 8)
        self.assertEqual(elements[0].name, "p")
        self.assertEqual(elements[1].name, "h4")
        self.assertEqual(elements[2].name, "p")
        self.assertEqual(elements[3].name, "blockquote")
        self.assertEqual(elements[4].name, "p")

    @tag("images_helper")
    def test_generate_image_tags_can_create_tags_with_alternating_classes(self):
        
        bio1 = BiographyFactory()
        img1 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img2 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img3 = create_test_img('test_image_2.tif', bio=bio1) #landscape

        tags = generate_image_tags(bio1.images.all())
        
        self.assertEqual(len(tags), 3)

        self.assertTrue("float-right" in tags[0]["tag"] )
        self.assertTrue("float-left" in tags[1]["tag"] )
        self.assertTrue("float-right" in tags[2]["tag"] )

        self.assertEqual(tags[0]["after_para"], 1)
        self.assertEqual(tags[1]["after_para"], 3)
        self.assertEqual(tags[2]["after_para"], 5)

    @tag("images_helper")
    def test_insert_image_returns_an_image_tag_at_correct_paragraphs(self):

        bio1 = BiographyFactory()
        img1 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img2 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img3 = create_test_img('test_image_2.tif', bio=bio1) #landscape

        image_tags = generate_image_tags(bio1.images.all())

        tag = insert_image(1, image_tags)
        self.assertTrue("figure-img" in tag)
        tag = insert_image(3, image_tags)
        self.assertTrue("figure-img" in tag)
        tag = insert_image(5, image_tags)
        self.assertTrue("figure-img" in tag)

        tag = insert_image(2, image_tags)
        self.assertEqual(tag, "")
        tag = insert_image(4, image_tags)
        self.assertEqual(tag, "")
     
    @tag("images_helper")
    def test_body_with_images_inserts_images_if_images_present(self):

        bio1 = BiographyFactory(body=sample_body_1)
        img1 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img2 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img3 = create_test_img('test_image_2.tif', bio=bio1) #landscape
        img1.caption="Caption1"
        img1.save()
        img2.caption="Caption2"
        img2.save()
        img3.caption="Caption3"
        img3.save()

        soup = BeautifulSoup(bio1.body_with_images(), "html.parser")
        tags = soup.find_all(True, recursive=False)
        self.assertNotEqual(bio1.body, bio1.body_with_images())
        self.assertEqual(len(tags), 11)

        self.assertEqual(tags[0].name, "p")
        self.assertIsNotNone(tags[1].find('img'))
        self.assertIsNotNone(tags[1].find('figcaption'))
        self.assertTrue(tags[1].find('figcaption').text.strip().endswith("Caption1"))
         
        self.assertIsNotNone(tags[6].find('img'))
        self.assertIsNotNone(tags[6].find('figcaption'))
        self.assertTrue(tags[6].find('figcaption').text.strip().endswith("Caption2"))

        self.assertIsNotNone(tags[9].find('img'))
        self.assertIsNotNone(tags[9].find('figcaption'))
        self.assertTrue(tags[9].find('figcaption').text.strip().endswith("Caption3"))

    @tag("images_helper")
    def test_body_with_images_makes_no_changes_to_body_if_no_images_present(self):
        bio1 = BiographyFactory(body=sample_body_1)

        body = BeautifulSoup(bio1.body, "html.parser")
        body_with_images = BeautifulSoup(bio1.body_with_images(), "html.parser")

        self.assertEqual(len(body.find_all(True, recursive=False)), len(body_with_images.find_all(True, recursive=False)))
