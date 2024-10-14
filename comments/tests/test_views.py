import json

from django.test import TestCase, tag
from django.urls import reverse

from biographies.models import *
from biographies.tests.factories import *

from comments.forms import SubmitCommentForm

class CommentsViewsTests(TestCase):

    @tag("comments_views")
    def  test_submit_comment_saves_comment_with_valid_data(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": ""
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(bio1.comments.count(), 1)


    @tag("comments_views")
    def  test_submit_comment_does_not_save_comment_if_url_populated(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": "a bot filled the form"
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success_")
        self.assertEqual(bio1.comments.count(), 0)

    @tag("comments_views")
    def  test_submit_comment_returns400_if_field_missing(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "comment": "A test comment",
            "url": "a bot filled the form"
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["status"], "data-error")
        self.assertEqual(bio1.comments.count(), 0)

    @tag("comments_views")
    def  test_submit_comment_returns405_if_not_POST(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data["status"], "method-error")
        self.assertEqual(bio1.comments.count(), 0)
