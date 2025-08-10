from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class AdminTests(TestCase):

    def setUp(self):
        password = "mypassword"
        User.objects.create_superuser("myuser", "myemail@test.com", password)


    def test_site_header(self):
        url = reverse("admin:index")
        self.client.login(username="myuser", password="mypassword")
        response = self.client.get(url)
        self.assertContains(response, text="DFB Admin", status_code=200)

    def test_site_title(self):
        url = reverse("admin:login")
        response = self.client.get(url)
        self.assertContains(response, text="DFB Admin", status_code=200)
