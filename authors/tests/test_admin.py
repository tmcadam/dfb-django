import re
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from authors.models import Author

class AdminTests(TestCase):

    def setUp(self):
        password = "mypassword"
        User.objects.create_superuser("myuser", "myemail@test.com", password)


    def test_authors_page_in_admin_index(self):
        url = reverse("admin:index")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Authors", status_code=200)

    def test_authors_has_admin_changelist(self):
        url = reverse("admin:authors_author_changelist")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Authors", status_code=200)
        self.assertContains(response, text="Select author to change", status_code=200)

    def test_authors_changelist_has_correct_columns(self):
        url = reverse("admin:authors_author_changelist")
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the table!
        Author.objects.create(first_name="Bob", last_name="Author1")

        response = self.client.get(url)
        self.assertContains(response, text="Authors", status_code=200)
        self.assertContains(response, text="Author", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', {"id": "result_list"})
        self.assertIsNotNone(table)

        # Check for the search form
        self.assertTrue(soup.find("input", {"value": "Search"}))

        # Check for the columns in the table
        self.assertTrue("Author" in table.find("thead").find_all("th")[1].text.strip())
        self.assertTrue("Short biography" in table.find("thead").find_all("th")[2].text.strip())


    def test_authors_admin_change_page(self):

        url = reverse("admin:authors_author_change", args=(1,))
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the change page!
        Author.objects.create(first_name="Bob", last_name="Author1")

        response = self.client.get(url)
        self.assertContains(response, text="Change author", status_code=200)
        self.assertContains(response, text="Author1, Bob", status_code=200)
        # check for the form fields
        self.assertContains(response, text="First name:", status_code=200)
        self.assertContains(response, text="Last name:", status_code=200)
        self.assertContains(response, text="Biography:", status_code=200)
