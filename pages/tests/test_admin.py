import re
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from comments.models import Comment
from pages.models import Page
from biographies.tests.factories import BiographyFactory

class PageAdminTests(TestCase):

    def setUp(self):
        password = "mypassword"
        User.objects.create_superuser("myuser", "myemail@test.com", password)


    def test_pages_page_in_admin_index(self):
        url = reverse("admin:index")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Pages", status_code=200)


    def test_pages_has_admin_changelist(self):
        url = reverse("admin:pages_page_changelist")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Pages", status_code=200)
        self.assertContains(response, text="Select page to change", status_code=200)


    def test_pages_changelist_has_correct_columns(self):
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the table!
        Page.objects.create(title="Test Page", slug="test-page", body="This is a test page.")

        url = reverse("admin:pages_page_changelist")
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', {"id": "result_list"})
        self.assertIsNotNone(table)

        # Check for the columns in the table
        self.assertTrue("Title" in table.find("thead").find_all("th")[1].text.strip())
        self.assertTrue("Page link" in table.find("thead").find_all("th")[2].text.strip())


    def test_pages_admin_change_page(self):

        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the change page!
        page = Page.objects.create(title="Test Page", slug="test-page", body="This is a test page.")

        url = reverse("admin:pages_page_change", args=(page.id,))
        response = self.client.get(url)
        self.assertContains(response, text="Change page", status_code=200)
        # check for the form fields
        self.assertContains(response, text="Title:", status_code=200)
        self.assertContains(response, text="Slug:", status_code=200)
        self.assertContains(response, text="Body:", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find('div', {"class": "summernote-div"}))
