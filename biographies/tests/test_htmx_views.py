from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

from biographies.tests.factories import BiographyFactory, CountryFactory
from biographies.models import Country
from authors.tests.factories import AuthorFactory
from authors.models import Author


def add_message(request, message):
    """Add a message to the request for testing."""
    if not hasattr(request, '_messages'):
        request._messages = FallbackStorage(request)


class ValidateSlugTests(TestCase):
    """Test validate_slug view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_htmx_views")
    def test_validate_slug_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:validate_slug')
        response = self.client.get(url, {'slug': 'test-slug'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_htmx_views")
    def test_validate_slug_returns_available_for_valid(self):
        """Valid, unused slug should return available message."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:validate_slug')
        response = self.client.get(url, {'slug': 'valid-slug'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('available', response.content.decode())

    @tag("biographies_htmx_views")
    def test_validate_slug_returns_unavailable_for_duplicate(self):
        """Existing slug should return unavailable message."""
        bio = BiographyFactory.create(slug='existing-slug')
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:validate_slug')
        response = self.client.get(url, {'slug': 'existing-slug'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('already in use', response.content.decode())

    @tag("biographies_htmx_views")
    def test_validate_slug_returns_invalid_format(self):
        """Invalid format slug should return format error."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:validate_slug')
        response = self.client.get(url, {'slug': 'Invalid_Slug'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid format', response.content.decode())


class AddCountryHtmxTests(TestCase):
    """Test add_country_htmx view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_htmx_views")
    def test_add_country_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:add_country_htmx')
        response = self.client.post(url, {'name': 'New Country'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_htmx_views")
    def test_add_country_requires_post(self):
        """GET request should return 405."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_country_htmx')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    @tag("biographies_htmx_views")
    def test_add_country_creates_country(self):
        """POST request should create a new country."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_country_htmx')
        response = self.client.post(url, {'name': 'New Country'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Country.objects.filter(name='New Country').exists())

    @tag("biographies_htmx_views")
    def test_add_country_returns_error_for_duplicate(self):
        """POST request with existing country should return error."""
        country = CountryFactory.create(name='Existing Country')
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_country_htmx')
        response = self.client.post(url, {'name': 'existing country'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('already exists', response.content.decode())


class AddAuthorHtmxTests(TestCase):
    """Test add_author_htmx view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_htmx_views")
    def test_add_author_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:add_author_htmx')
        response = self.client.post(url, {'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_htmx_views")
    def test_add_author_requires_post(self):
        """GET request should return 405."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_author_htmx')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    @tag("biographies_htmx_views")
    def test_add_author_creates_author(self):
        """POST request should create a new author."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_author_htmx')
        response = self.client.post(url, {'first_name': 'John', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Author.objects.filter(first_name='John', last_name='Doe').exists())

    @tag("biographies_htmx_views")
    def test_add_author_returns_error_for_duplicate(self):
        """POST request with existing author should return error."""
        author = AuthorFactory.create(first_name='John', last_name='Doe')
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_author_htmx')
        response = self.client.post(url, {'first_name': 'john', 'last_name': 'doe'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('already exists', response.content.decode())

    @tag("biographies_htmx_views")
    def test_add_author_returns_error_without_last_name(self):
        """POST request without last name should return error."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:add_author_htmx')
        response = self.client.post(url, {'first_name': 'John', 'last_name': ''})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue('required' in content.lower() or 'Last name' in content)
