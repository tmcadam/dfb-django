import re
import tempfile
from datetime import datetime as dt, timedelta as td, timezone as tz

from bs4 import BeautifulSoup

from django.template import loader
from django.test import TestCase, tag, override_settings
from django.conf import settings

from biographies.tests.factories import BiographyFactory

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class CommentTemplateTests(TestCase):

## Revisions

    @tag("comments_template")
    def test_comments_fragment_shows_only_approved_comments(self):

        bio1 = BiographyFactory.create(title="Bio1")
        comment1 = bio1.comments.create(name="Joe", email="joe@blah.com", comment="Comment 1")
        comment2 = bio1.comments.create(name="Tom", email="tom@blah.com", comment="Comment 2")
        comment3 = bio1.comments.create(name="Sam", email="sam@blah.com", comment="Comment 3")

        comment1.approved=True
        comment1.created_at = dt.now(tz.utc) - td(days=3)
        comment1.save()
        comment3.approved=True
        comment3.created_at = dt.now(tz.utc) - td(days=7)
        comment3.save()

        template = loader.get_template("comments/_comments.html")
        rendered = template.render({"biography": bio1})
        soup = BeautifulSoup(rendered, "html.parser")

        comments_div = soup.find('div', class_="biography_comments_wrapper")
        self.assertIsNotNone(comments_div)
        comment_titles = comments_div.find_all('h5', class_="card-title")
        self.assertEqual(len(comment_titles), 2)

        self.assertIsNotNone(comments_div.find('h5', class_="card-title", text="Joe"))
        self.assertIsNotNone(comments_div.find('h5', class_="card-title", text="Sam"))
        # Tom's comment shouldn't be displayed, as not approved
        self.assertIsNone(comments_div.find('h5', class_="card-title", text="Tom"))

        # ordering
        self.assertEqual(comment_titles[0].text, "Sam")
        self.assertEqual(comment_titles[1].text, "Joe")

    @tag("comments_template")
    def test_comments_fragment_still_rendered_if_no_comments(self):

        bio1 = BiographyFactory.create(title="Bio1")
        
        template = loader.get_template("comments/_comments.html")
        rendered = template.render({"biography": bio1})
        soup = BeautifulSoup(rendered, "html.parser")
        
        comments_div = soup.find('div', class_="biography_comments_wrapper")
        self.assertIsNotNone(comments_div)
        self.assertIsNotNone(comments_div.find('h4', text="Comments"))
        self.assertIsNotNone(comments_div.find('button'))
                             
    @tag("comments_template")
    def test_malicious_comment_not_rendered(self):

        bio1 = BiographyFactory.create(title="Bio1")
        comment1 = bio1.comments.create(
            name="Sam", 
            email="sam@blah.com", 
            comment="""<script>document.getElementById("demo").innerHTML = "Hello JavaScript!";</script>"""
            )

        comment1.approved=True
        comment1.save()

        template = loader.get_template("comments/_comments.html")
        rendered = template.render({"biography": bio1})
        soup = BeautifulSoup(rendered, "html.parser")

        self.assertIsNone(soup.find('script'))
