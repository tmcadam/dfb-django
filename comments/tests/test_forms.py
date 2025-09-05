import tempfile

from bs4 import BeautifulSoup

from django.template import loader
from django.test import TestCase, tag, override_settings
from django.conf import settings
from django.urls import reverse

from biographies.tests.factories import BiographyFactory

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class CommentFormTests(TestCase):


    @tag("comments_form")
    def test_comments_form_has_crsf_token_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        crsf_input = form.find('input', {"name": "csrfmiddlewaretoken", "type": "hidden"})
        self.assertIsNotNone(crsf_input)


    @tag("comments_form")
    def test_comments_form_has_name_input_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        name_label = form.find('label', {"for": "id_name"})
        self.assertEqual(name_label.text.strip(), "Name*")
        name_input = form.find('input', {"id": "id_name", "type": "text"})
        self.assertIsNotNone(name_input)
        name_helper = form.find('small', {"id": "id_name_helptext"})
        self.assertEqual(name_helper.text.strip(), "Name displayed with the comment (required).")


    @tag("comments_form")
    def test_comments_form_has_email_input_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        email_label = form.find('label', {"for": "id_email"})
        self.assertEqual(email_label.text.strip(), "Email*")
        email_input = form.find('input', {"id": "id_email", "type": "email"})
        self.assertIsNotNone(email_input)
        email_helper = form.find('small', {"id": "id_email_helptext"})
        self.assertEqual(email_helper.text.strip(), "This will not be displayed publically (required).")


    @tag("comments_form")
    def test_comments_form_has_comment_input_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        comment_label = form.find('label', {"for": "id_comment"})
        self.assertEqual(comment_label.text.strip(), "Comment*")
        comment_input = form.find('textarea', {"id": "id_comment"})
        self.assertIsNotNone(comment_input)


    @tag("comments_form")
    def test_comments_form_has_hidden_biography_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        biography_input = form.find('input', {"name": "biography", "type": "hidden"})
        self.assertIsNotNone(biography_input)
        self.assertEqual(biography_input["value"], str(bio1.id))

    @tag("comments_form")
    def test_comments_form_has_hidden_url_field(self):

        bio1 = BiographyFactory.create(title="Bio1", slug="bio1")
        url = reverse('biographies:show', args=["bio1"])
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        comments_div = soup.find('div', id="comments-form-modal")
        self.assertIsNotNone(comments_div)

        form = comments_div.find('form')
        self.assertIsNotNone(form)

        # this is the id that is refrenced in css to hide this field
        wrapper_div = form.find('div', {"id": "div_id_url", "class": "form-group"})
        self.assertIsNotNone(wrapper_div)
        url_input = wrapper_div.find('input', {"id": "id_url", "type": "text"})
        self.assertIsNotNone(url_input)
        self.assertNotIn("value", url_input.attrs)

