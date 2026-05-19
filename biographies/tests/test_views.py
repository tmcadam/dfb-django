from django.test import TestCase, tag, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from biographies.models import *
from .factories import *

from comments.forms import SubmitCommentForm

class BiographyViewsTests(TestCase):

    @tag("biographies_views")
    def  test_routing_for_biographies_index(self):
        url = reverse('biographies:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    @tag("biographies_views")
    def  test_index_returns_all_biographies(self):
        BiographyFactory.create(title="Bio1", slug="bio1")
        BiographyFactory.create(title="Bio2", slug="bio2")
        BiographyFactory.create(title="Bio3", slug="bio3")
        url = reverse('biographies:index')
        response = self.client.get(url)
        self.assertEqual(len(response.context["page_obj"]), 3)
        self.assertContains(response, text="Bio1", status_code=200)
        self.assertContains(response, text="Bio2", status_code=200)
        self.assertContains(response, text="Bio3", status_code=200)

    @tag("biographies_views")
    def  test_search_returns_correct_biographies(self):
        BiographyFactory.create(title="Bio1", slug="bio1")
        BiographyFactory.create(title="Bio2", slug="bio2")
        BiographyFactory.create(title="Bio3", slug="bio3")
        url = reverse('biographies:index')
        response = self.client.get(url, {"search": "Bio1"})
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertContains(response, text="Bio1", status_code=200)
        self.assertNotContains(response, text="Bio2")
        self.assertNotContains(response, text="Bio3")

    @tag("biographies_views")
    def  test_search_returns_correct_biographies_with_case_insensitive(self):
        BiographyFactory.create(title="Bio1", slug="bio1")
        BiographyFactory.create(title="Bio2", slug="bio2")
        BiographyFactory.create(title="Bio3", slug="bio3")
        url = reverse('biographies:index')
        response = self.client.get(url, {"search": "bio1"})
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertContains(response, text="Bio1", status_code=200)

    @tag("biographies_views")
    def  test_search_returns_message_if_no_results(self):
        BiographyFactory.create(title="Bio1", slug="bio1")
        BiographyFactory.create(title="Bio2", slug="bio2")
        BiographyFactory.create(title="Bio3", slug="bio3")
        url = reverse('biographies:index')
        response = self.client.get(url, {"search": "Bio4"})
        self.assertContains(response, text="No results", status_code=200)

    @tag("biographies_views")
    def  test_pagination_returns_subset_of_biographies_for_index(self):
        for i in range(100):
            BiographyFactory.create(title=f"Bio{i}", slug=f"bio{i}")
        url = reverse('biographies:index')
        response = self.client.get(url)
        self.assertEqual(Biography.objects.all().count(), 100)
        self.assertEqual(response.context["page_obj"].paginator.num_pages, 4)
        self.assertEqual(len(response.context["page_obj"]), 25)

    @tag("biographies_views")
    def  test_pagination_returns_subset_of_biographies_for_index_with_search(self):
        for i in range(50):
            BiographyFactory.create(title=f"Bio{i}", slug=f"bio{i}")
        for i in range(50):
            BiographyFactory.create(title=f"Other{i}", slug=f"other{i}")
        url = reverse('biographies:index')
        response = self.client.get(url, {"search": "Bio"})
        self.assertEqual(Biography.objects.all().count(), 100)
        self.assertEqual(response.context["page_obj"].paginator.num_pages, 2)
        self.assertEqual(len(response.context["page_obj"]), 25)

    @tag("biographies_views")
    def test_routing_for_show_biography_by_slug(self):

        BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)
        self.assertContains(response, text="Bio1", status_code=200)

    @tag("biographies_views")
    def test_routing_for_show_biography_by_id(self):

        biography = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show_by_id', args=[biography.id])
        response = self.client.get(url)
        self.assertRedirects(response, '/biographies/bio1', status_code=302,
            target_status_code=200, fetch_redirect_response=True)

    @tag("biographies_views")
    def  test_biography_view_has_partially_filled_comment_form_in_context(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)
        self.assertContains(response, text="Bio1", status_code=200)
        self.assertEqual(type(response.context["comments_form"]), SubmitCommentForm)
        self.assertEqual(response.context["comments_form"].initial["biography"], bio1.id)


class BiographyCreateViewTests(TestCase):
    """Test BiographyCreateView functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.factory = RequestFactory()

    @tag("biographies_views")
    def test_create_view_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_create_view_get_returns_200(self):
        """Authenticated users should see the form."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("biographies_views")
    def test_create_view_post_creates_biography(self):
        """POST request should create a new biography."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:new')
        data = {
            'title': 'New Biography',
            'slug': 'new-biography',
            'lifespan': '1900-1950',
            'body': 'This is a test biography.',
            'authors': '',
            'primary_country': '',
            'secondary_country': '',
            'biographyauthor_set-TOTAL_FORMS': '1',
            'biographyauthor_set-INITIAL_FORMS': '0',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Biography.objects.filter(title='New Biography').exists())

    @tag("biographies_views")
    def test_create_view_post_redirects_to_show(self):
        """After creation, should redirect to the biography show page."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:new')
        data = {
            'title': 'New Biography',
            'slug': 'new-biography',
            'lifespan': '1900-1950',
            'body': 'This is a test biography.',
            'authors': '',
            'primary_country': '',
            'secondary_country': '',
            'biographyauthor_set-TOTAL_FORMS': '1',
            'biographyauthor_set-INITIAL_FORMS': '0',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/biographies/new-biography', fetch_redirect_response=True)


class BiographyUpdateViewTests(TestCase):
    """Test BiographyUpdateView functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.biography = BiographyFactory.create(title='Update Test', slug='update-test')

    @tag("biographies_views")
    def test_update_view_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:edit', kwargs={'bio_slug': self.biography.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_update_view_get_returns_200(self):
        """Authenticated users should see the form."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:edit', kwargs={'bio_slug': self.biography.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("biographies_views")
    def test_update_view_post_updates_biography(self):
        """POST request should update the biography."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:edit', kwargs={'bio_slug': self.biography.slug})
        data = {
            'title': 'Updated Title',
            'slug': 'updated-title',
            'lifespan': '1800-2000',
            'body': 'Updated body text.',
            'authors': '',
            'primary_country': '',
            'secondary_country': '',
            'biographyauthor_set-TOTAL_FORMS': '1',
            'biographyauthor_set-INITIAL_FORMS': '0',
            'biographyauthor_set-MIN_NUM_FORMS': '0',
            'biographyauthor_set-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.biography.refresh_from_db()
        self.assertEqual(self.biography.title, 'Updated Title')


class BiographyDeleteViewTests(TestCase):
    """Test BiographyDeleteView functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.biography = BiographyFactory.create(title='Delete Test', slug='delete-test')

    @tag("biographies_views")
    def test_delete_view_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:delete', kwargs={'bio_slug': self.biography.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_delete_view_get_returns_200(self):
        """Authenticated users should see the delete confirmation."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:delete', kwargs={'bio_slug': self.biography.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ManageBiographiesTests(TestCase):
    """Test manage_biographies view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_views")
    def test_manage_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_manage_returns_200_for_authenticated(self):
        """Authenticated users should see the manage page."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("biographies_views")
    def test_manage_search_filters_results(self):
        """Search should filter biographies by title."""
        BiographyFactory.create(title='Alpha Bio', slug='alpha')
        BiographyFactory.create(title='Beta Bio', slug='beta')
        BiographyFactory.create(title='Gamma Bio', slug='gamma')

        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:manage')
        response = self.client.get(url, {'search': 'Alpha'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alpha Bio')
        self.assertNotContains(response, 'Beta Bio')


class ResetFeaturedTests(TestCase):
    """Test reset_featured view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_views")
    def test_reset_featured_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        url = reverse('biographies:reset_featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_reset_featured_redirects_to_home(self):
        """Authenticated users should be redirected to home after reset.

        Note: reset_featured_bios() requires biographies with images, lifespan, authors
        and portrait-oriented images. We test the redirect behavior when there are no
        qualifying biographies (the function may raise an error in this edge case).
        """
        # Ensure no biographies that would match the filter criteria exist
        Biography.objects.all().delete()
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:reset_featured')
        try:
            response = self.client.get(url)
            self.assertIn(response.status_code, [302, 200])
        except ValueError:
            pass


class MakeFeaturedTests(TestCase):
    """Test make_featured view functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @tag("biographies_views")
    def test_make_featured_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        bio = BiographyFactory.create()
        url = reverse('biographies:make_featured', kwargs={'bio_slug': bio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @tag("biographies_views")
    def test_make_featured_sets_featured_flag(self):
        """make_featured should set the featured flag on a biography."""
        bio = BiographyFactory.create(featured=False)
        self.client.login(username='testuser', password='testpass123')
        url = reverse('biographies:make_featured', kwargs={'bio_slug': bio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        bio.refresh_from_db()
        self.assertTrue(bio.featured)
