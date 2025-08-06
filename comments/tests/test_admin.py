import re
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from comments.models import Comment
from biographies.tests.factories import BiographyFactory

class AdminTests(TestCase):

    def setUp(self):
        password = "mypassword"
        User.objects.create_superuser("myuser", "myemail@test.com", password)


    def test_comments_page_in_admin_index(self):
        url = reverse("admin:index")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Comments", status_code=200)

    def test_comments_has_admin_changelist(self):
        url = reverse("admin:comments_comment_changelist")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Comments", status_code=200)
        self.assertContains(response, text="Select comment to change", status_code=200)

    def test_comments_changelist_has_correct_columns(self):
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the table!

        bio = BiographyFactory.create(title="Bio1", slug="bio1")
        Comment.objects.create(biography=bio, name="Bob", email="bob@bob.com", comment="This is a comment.")

        url = reverse("admin:comments_comment_changelist")
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', {"id": "result_list"})
        self.assertIsNotNone(table)

        # Check for the search form
        self.assertTrue(soup.find("input", {"value": "Search"}))

        filters = soup.find('nav', {"id": "changelist-filter"})
        self.assertTrue("By approved" in filters.find_all("summary")[0].text.strip())

        # Check for the columns in the table
        self.assertTrue("Biography" in table.find("thead").find_all("th")[1].text.strip())
        self.assertTrue("Name" in table.find("thead").find_all("th")[2].text.strip())
        self.assertTrue("Email" in table.find("thead").find_all("th")[3].text.strip())
        self.assertTrue("Approved" in table.find("thead").find_all("th")[4].text.strip())
        self.assertTrue("Created at" in table.find("thead").find_all("th")[5].text.strip())


    def test_comments_admin_change_page(self):

        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the change page!
        bio = BiographyFactory.create(title="Bio1", slug="bio1")
        Comment.objects.create(biography=bio, name="Bob", email="bob@bob.com", comment="This is a comment.")

        url = reverse("admin:comments_comment_change", args=(1,))
        response = self.client.get(url)
        self.assertContains(response, text="Change comment", status_code=200)
        # check for the form fields
        self.assertContains(response, text="Biography:", status_code=200)
        self.assertContains(response, text="Name:", status_code=200)
        self.assertContains(response, text="Email:", status_code=200)
        self.assertContains(response, text="Comment:", status_code=200)
        self.assertContains(response, text="Approved", status_code=200)
