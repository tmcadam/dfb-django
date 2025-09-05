import tempfile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from bs4 import BeautifulSoup

from images.models import Image
from images.tests.utils import create_test_img

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ImageAdminTests(TestCase):

    def setUp(self):
        password = "mypassword"
        User.objects.create_superuser("myuser", "myemail@test.com", password)


    def test_images_page_in_admin_index(self):
        url = reverse("admin:index")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Images", status_code=200)


    def test_images_has_admin_changelist(self):
        url = reverse("admin:images_image_changelist")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Images", status_code=200)
        self.assertContains(response, text="Select image to change", status_code=200)


    def test_images_changelist_has_correct_columns(self):
        url = reverse("admin:images_image_changelist")
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the table!
        create_test_img('test_image_1.jpg')

        response = self.client.get(url)
        self.assertContains(response, text="Images", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', {"id": "result_list"})
        self.assertIsNotNone(table)

        # Check for the search form
        self.assertTrue(soup.find("input", {"value": "Search"}))

        # Check for the columns in the table
        self.assertTrue("Biography  title" in table.find("thead").find_all("th")[1].text.strip())
        self.assertTrue("Title" in table.find("thead").find_all("th")[2].text.strip())
        self.assertTrue("Thumbnail" in table.find("thead").find_all("th")[3].text.strip())


    def test_images_admin_change_page(self):

        img = create_test_img('test_image_1.jpg')

        url = reverse("admin:images_image_change", args=(img.id,))
        self.client.login(username="myuser", password="mypassword")

        response = self.client.get(url)
        self.assertContains(response, text="Change image", status_code=200)
        self.assertContains(response, text="Image Title", status_code=200)
        # check for the form fields
        self.assertContains(response, text="Title:", status_code=200)
        self.assertContains(response, text="Caption:", status_code=200)
        self.assertContains(response, text="Attribution:", status_code=200)
        self.assertContains(response, text="Biography:", status_code=200)
        self.assertContains(response, text="Image:", status_code=200)
        self.assertContains(response, text="Attribution:", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find('div', {"class": "summernote-div"}))
