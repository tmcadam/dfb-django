from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from biographies.models import Country
from biographies.models import Biography
from biographies.tests.factories import BiographyFactory
from bs4 import BeautifulSoup


class CountryAdminViewsTests(TestCase):


    def setUp(self):
        password = 'mypassword'
        User.objects.create_superuser('myuser', 'myemail@test.com', password)


    def test_countries_page_in_admin(self):
        url = reverse('admin:biographies_country_changelist')
        self.client.login(username='myuser', password='mypassword')
        response = self.client.get(url)
        self.assertContains(response, text='Select country to change', status_code=200)

    def test_countries_has_admin_changelist(self):
        url = reverse('admin:biographies_country_changelist')
        self.client.login(username='myuser', password='mypassword')
        response = self.client.get(url)
        self.assertContains(response, text='Countries', status_code=200)
        self.assertContains(response, text='Select country to change', status_code=200)

    def test_countries_changelist_has_correct_columns(self):
        url = reverse('admin:biographies_country_changelist')
        self.client.login(username='myuser', password='mypassword')

        Country.objects.create(name="Test Country")

        response = self.client.get(url)
        self.assertContains(response, text='Countries', status_code=200)

        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'id': 'result_list'})
        self.assertIsNotNone(table)

        # Check for the columns in the table
        self.assertTrue('Country' in table.find('thead').findAll('th')[1].text.strip())


    def test_countries_admin_change_page(self):

        country = Country.objects.create(name="Test Country")

        url = reverse('admin:biographies_country_change', args=(country.id,))
        self.client.login(username='myuser', password='mypassword')

        # Need an object to create the change page!

        response = self.client.get(url)
        self.assertContains(response, text='Change country', status_code=200)
        self.assertContains(response, text='Name:', status_code=200)


class BiographiesAdminViewsTests(TestCase):


    def setUp(self):
        password = 'mypassword'
        User.objects.create_superuser('myuser', 'myemail@test.com', password)


    def test_biographies_page_in_admin(self):
        url = reverse('admin:biographies_biography_changelist')
        self.client.login(username='myuser', password='mypassword')
        response = self.client.get(url)
        self.assertContains(response, text='Select biography to change', status_code=200)


    def test_biographies_has_admin_changelist(self):
        url = reverse("admin:biographies_biography_changelist")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="Biographies", status_code=200)
        self.assertContains(response, text="Select biography to change", status_code=200)


    def test_biographies_changelist_has_correct_columns(self):

        url = reverse("admin:biographies_biography_changelist")
        self.client.login(username="myuser", password="mypassword")

        # Need an object to create the table!
        BiographyFactory.create(title="Bio1", slug="bio1")

        response = self.client.get(url)
        self.assertContains(response, text="Biographies", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', {"id": "result_list"})
        self.assertIsNotNone(table)

        # Check for the search form
        self.assertTrue(soup.find("input", {"value": "Search"}))

        # Check for the columns in the table

        columns = [c.text.strip().upper() for c in table.find("thead").find_all("th")]

        self.assertTrue("TITLE" in columns)
        self.assertTrue("AUTHORS" in columns)
        self.assertTrue("SOUTH GEORGIA" in columns)
        self.assertTrue("FEATURED" in columns)
        self.assertTrue("BIOGRAPHY LINK" in columns)


    def test_biographies_admin_change_page(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")

        url = reverse("admin:biographies_biography_change", args=(bio1.id,))
        self.client.login(username="myuser", password="mypassword")

        response = self.client.get(url)

        self.assertContains(response, text="Change biography", status_code=200)

        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find('div', {"id": "content"})

        section_headers = [c.text.strip().upper() for c in content.find_all('h2')[1:]]
        field_labels = [c.text.strip().upper() for c in content.find_all('label')]
        inline_labels  = [c.text.strip().upper() for c in content.find_all('th')]

        self.assertTrue("BODY" in section_headers)
        self.assertTrue("ADDITIONAL INFORMATION" in section_headers)
        self.assertTrue("AUTHORS" in section_headers)
        self.assertTrue("COMMENTS" in section_headers)
        self.assertTrue("IMAGES" in section_headers)

        self.assertTrue("TITLE:" in field_labels)
        self.assertTrue("FEATURED" in field_labels)
        self.assertTrue("BIOGRAPHY LINK:" in field_labels)
        self.assertTrue("LIFESPAN:" in field_labels)
        self.assertTrue("SLUG:" in field_labels)
        self.assertTrue("PRIMARY COUNTRY:" in field_labels)
        self.assertTrue("SECONDARY COUNTRY:" in field_labels)
        self.assertTrue("SOUTH GEORGIA" in field_labels)
        self.assertTrue("AUTHORS:" in field_labels)
        self.assertTrue("BODY:" in field_labels)
        self.assertTrue("EXTERNAL LINKS:" in field_labels)
        self.assertTrue("REFERENCES:" in field_labels)
        self.assertTrue("REVISIONS:" in field_labels)
        # inline comment form
        self.assertTrue("NAME:" in field_labels)
        self.assertTrue("EMAIL:" in field_labels)
        self.assertTrue("COMMENT:" in field_labels)
        self.assertTrue("CREATED AT:" in field_labels)
        self.assertTrue("APPROVED" in field_labels)
        # authors inline
        self.assertTrue("AUTHOR" in inline_labels)
        self.assertTrue("AUTHOR POSITION" in inline_labels)
        # images inline
        self.assertTrue("TITLE" in inline_labels)
        self.assertTrue("CAPTION" in inline_labels)
        self.assertTrue("THUMBNAIL" in inline_labels)

        # Check for the summernote editor
        self.assertEqual(len(soup.find_all('div', {"class": "summernote-div"})), 3)
