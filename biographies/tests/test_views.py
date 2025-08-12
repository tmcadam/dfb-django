from django.test import TestCase, tag
from django.urls import reverse

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

