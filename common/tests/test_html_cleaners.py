from unittest import skip
from django.test import TestCase, tag
from biographies.tests.factories import BiographyFactory
from common.html_cleaners import *

class HtmlCleanerTests(TestCase):

    @tag("helpers")
    def test_clean_urls_removes_protocol_and_host_from_string(self):
        BiographyFactory.create(slug="some-bio")
        test_strs = [
            "<p>before <a href=\"https://www.falklandsbiographies.org/biographies/some-bio\">after</a></p>",
            "<p>before <a href=\"https://falklandsbiographies.org/biographies/some-bio\">after</a></p>",
            "<p>before <a href=\"/biographies/some-bio\">after</a></p>"
            ]
        for test_str in test_strs:
            self.assertEqual(clean_urls(test_str), "<p>before <a href=\"/biographies/some-bio\">after</a></p>")

    #@skip("Skip until fixed")
    @tag("helpers")
    def test_clean_urls_ignores_any_external_urls(self):
        test_strs = ["<p>before <a href=\"http://www.wikipedia.com/test-url\">after</a></p>",
                     "<p>before <a href=\"http://www.some-webpage.com/biographies/test-url\">after</a></p>"]
        for test_str in test_strs:
            self.assertEqual(clean_urls(test_str), test_str)
