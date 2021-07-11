from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

class AdminViewsTests(TestCase):

    def setUp(self):
        password = 'mypassword' 
        User.objects.create_superuser('myuser', 'myemail@test.com', password)

    def test_biographies_page_in_admin(self):
        url = reverse('admin:biographies_biography_changelist')
        self.client.login(username='myuser', password='mypassword')
        response = self.client.get(url)
        self.assertContains(response, text='Select biography to change', status_code=200)

    def test_countries_page_in_admin(self):
        url = reverse('admin:biographies_country_changelist')
        self.client.login(username='myuser', password='mypassword')
        response = self.client.get(url)
        self.assertContains(response, text='Select country to change', status_code=200)