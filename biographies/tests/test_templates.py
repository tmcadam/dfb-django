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

## Revisions

    @tag("biographies_template")
    def test_revisions_fragment_has_correct_revisions_text(self):

        biography = BiographyFactory(revisions="Rev1\r\nRev2")

        template = loader.get_template("biographies/show/_revisions.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        revisions_div = soup.find('div', class_="biography_revsions")
        self.assertIsNotNone(revisions_div)
        self.assertTrue(revisions_div.find_all("br"))
        self.assertTrue("Rev1" in revisions_div.text)
        self.assertTrue("Rev2" in revisions_div.text)

    @tag("biographies_template")
    def test_revisions_shown_if_revisions(self):

        biography = BiographyFactory(revisions="A revision")

        template = loader.get_template("biographies/show/_revisions.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        revisions_div = soup.find('div', class_="biography_revsions")
        revisions_h4 = soup.find('h4', string="Revisions")

        self.assertIsNotNone(revisions_h4)
        self.assertIsNotNone(revisions_div)


    @tag("biographies_template")
    def test_revisions_not_shown_if_revisions_is_None(self):

        biography = BiographyFactory(revisions=None)

        template = loader.get_template("biographies/show/_revisions.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        revisions_div = soup.find('div', class_="biography_revsions")
        revisions_h4 = soup.find('h4', string="Revisions")

        self.assertIsNone(revisions_h4)
        self.assertIsNone(revisions_div)


    @tag("biographies_template")
    def test_revisions_not_shown_if_revisions_is_empty(self):
        """
        Whitespace is stripped on save so shouldn't need to worry about a whitespace string
        """
        biography = BiographyFactory(revisions="")

        template = loader.get_template("biographies/show/_revisions.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        revisions_div = soup.find('div', class_="biography_revsions")
        revisions_h4 = soup.find('h4', string="Revisions")

        self.assertIsNone(revisions_h4)
        self.assertIsNone(revisions_div)

## References

    @tag("biographies_template")
    def test_references_shown_if_references(self):

        biography = BiographyFactory(references="A reference")

        template = loader.get_template("biographies/show/_references.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        references_div = soup.find('div', class_="biography_references")
        references_h4 = soup.find('h4', string="References")

        self.assertIsNotNone(references_h4)
        self.assertIsNotNone(references_div)

    @tag("biographies_template")
    def test_references_shown_if_references_is_None(self):

        biography = BiographyFactory(references=None)

        template = loader.get_template("biographies/show/_references.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        references_div = soup.find('div', class_="biography_references")
        references_h4 = soup.find('h4', string="References")

        self.assertIsNone(references_h4)
        self.assertIsNone(references_div)

    @tag("biographies_template")
    def test_references_not_shown_if_references_is_empty_string(self):
        """
        Whitespace is stripped on save so shouldn't need to worry about a whitespace string
        """
        biography = BiographyFactory(references="")

        template = loader.get_template("biographies/show/_references.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        references_div = soup.find('div', class_="biography_references")
        references_h4 = soup.find('h4', string="References")

        self.assertIsNone(references_h4)
        self.assertIsNone(references_div)

## External links

    @tag("biographies_template")
    def test_external_links_shown_if_external_links(self):

        biography = BiographyFactory(external_links="A external_link")

        template = loader.get_template("biographies/show/_external_links.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        external_links_div = soup.find('div', class_="biography_external_links")
        external_links_h4 = soup.find('h4', string="External links")

        self.assertIsNotNone(external_links_h4)
        self.assertIsNotNone(external_links_div)

    @tag("biographies_template")
    def test_external_links_not_shown_if_external_links_is_None(self):

        biography = BiographyFactory(external_links=None)

        template = loader.get_template("biographies/show/_external_links.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        external_links_div = soup.find('div', class_="biography_external_links")
        external_links_h4 = soup.find('h4', string="External links")

        self.assertIsNone(external_links_h4)
        self.assertIsNone(external_links_div)

    @tag("biographies_template")
    def test_external_links_not_shown_if_external_links_is_empty(self):

        biography = BiographyFactory(external_links="")

        template = loader.get_template("biographies/show/_external_links.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        external_links_div = soup.find('div', class_="biography_external_links")
        external_links_h4 = soup.find('h4', string="External links")

        self.assertIsNone(external_links_h4)
        self.assertIsNone(external_links_div)

## Authors

    @tag("biographies_template")
    def test_authors_shown_if_authors(self):

        biography = BiographyFactory(authors="A external_link")

        template = loader.get_template("biographies/show/_authors.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        authors_div = soup.find('div', class_="biography_authors")
        authors_h4 = soup.find('h4', string="Authors")

        self.assertIsNotNone(authors_h4)
        self.assertIsNotNone(authors_div)

    @tag("biographies_template")
    def test_authors_not_shown_if_authors_is_None(self):

        biography = BiographyFactory(authors=None)

        template = loader.get_template("biographies/show/_authors.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        authors_div = soup.find('div', class_="biography_authors")
        authors_h4 = soup.find('h4', string="Authors")

        self.assertIsNone(authors_h4)
        self.assertIsNone(authors_div)

    @tag("biographies_template")
    def test_authors_not_shown_if_authors_is_empty(self):

        biography = BiographyFactory(authors="")

        template = loader.get_template("biographies/show/_authors.html")
        rendered = template.render({"biography": biography})
        soup = BeautifulSoup(rendered, "html.parser")

        authors_div = soup.find('div', class_="biography_authors")
        authors_h4 = soup.find('h4', string="Authors")

        self.assertIsNone(authors_h4)
        self.assertIsNone(authors_div)