from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from pages.models import Page

class PagesViewsTests(TestCase):

    def test_home_page(self):
        """
        The home view of the DFB site returns a simple test string.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='The Dictionary of Falklands Biography', status_code=200)


    def test_footer_has_admin_link(self):
        """
        The footer contains a link to the admin page.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='/admin/', status_code=200)


    def test_page(self):
        """
        The page view returns a 200 status code.
        """
        Page.objects.create(
            title="Test Page",
            body="This is a test page.",
            slug="test-page"
        )

        url = reverse('pages:show', args=['test-page'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='Test Page', status_code=200)
        self.assertContains(response, text='This is a test page.', status_code=200)


    def test_bootstrap_present(self):
        """
        Bootstrap and jquey should be in the page head.
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='jquery', status_code=200)
        self.assertContains(response, text='bootstrap', status_code=200)


    def test_page_title(self):
        """
        The title of the page (browser tab) contains the environment name, unless in production.
        """
        url = reverse('pages:home')
        settings.ENVIRONMENT = 'staging'
        response = self.client.get(url)
        self.assertContains(response, text='DFB - Staging', status_code=200)
        settings.ENVIRONMENT = 'production'
        self.assertContains(response, text='DFB', status_code=200)
        self.assertNotContains(response, text='DFB - Production')


    def test_page_has_footer(self):
        """
        The home page contains a footer
        """
        url = reverse('pages:home')
        response = self.client.get(url)
        self.assertContains(response, text='David Tatham. All rights reserved.', status_code=200)

from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth.models import User

from pages.models import Page
from pages.forms import PageForm


class PageCreateViewTests(TestCase):
    """Test PageCreateView functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("pages_new_views")
    def test_page_create_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('pages:new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("pages_new_views")
    def test_page_create_get_returns_200(self):
        """Authenticated users should see the create form."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pages:new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("pages_new_views")
    def test_page_create_post_creates_page(self):
        """POST request should create a new page."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pages:new')
        data = {
            'title': 'New Page',
            'slug': 'new-page',
            'body': '<p>This is a new page.</p>',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Page.objects.filter(title='New Page').exists())


class PageUpdateViewTests(TestCase):
    """Test PageUpdateView functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.page = Page.objects.create(
            title='Update Test',
            slug='update-test',
            body='<p>Original content.</p>',
        )

    @tag("pages_new_views")
    def test_page_update_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('pages:edit', kwargs={'page_slug': self.page.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("pages_new_views")
    def test_page_update_get_returns_200(self):
        """Authenticated users should see the update form."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pages:edit', kwargs={'page_slug': self.page.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("pages_new_views")
    def test_page_update_post_updates_page(self):
        """POST request should update the page."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pages:edit', kwargs={'page_slug': self.page.slug})
        data = {
            'title': 'Updated Page',
            'slug': 'updated-page',
            'body': '<p>Updated content.</p>',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.page.refresh_from_db()
        self.assertEqual(self.page.title, 'Updated Page')
