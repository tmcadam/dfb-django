import re
import tempfile

from bs4 import BeautifulSoup

from django.template import loader
from django.test import TestCase, tag, override_settings
from django.conf import settings

from biographies.tests.factories import BiographyFactory

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class BiographyTemplateTests(TestCase):

## JS and CSS Tags

    @tag("biographies_template")
    def test_biography_template_has_css_tags(self):

        template = loader.get_template("biographies/show.html")
        rendered = template.render()
        soup = BeautifulSoup(rendered, "html.parser")

        self.assertTrue(soup.find_all('link', href=re.compile(r"(.*)ekko-lightbox\.css$")))

    @tag("biographies_template")
    def test_biography_template_has_js_tags(self):

        template = loader.get_template("biographies/show.html")
        rendered = template.render()
        soup = BeautifulSoup(rendered, "html.parser")

        self.assertTrue(soup.find_all('script', src=re.compile(r"(.*)ekko-lightbox.min\.js$")))
        self.assertTrue(soup.find_all('script', src=re.compile(r"(.*)biographies\.js$")))
        self.assertTrue(soup.find_all('script', src=re.compile(r"(.*)lightbox\.js$")))

