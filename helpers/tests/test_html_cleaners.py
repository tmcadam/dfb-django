from unittest import TestCase as SimpleTestCase
from helpers.html_cleaners import *

from django.test import tag

class ImageUnitTests(SimpleTestCase):

    @tag("helpers")
    def test_clean_urls_removes_protocol_and_host_from_string(self):
        test_strs = [   
            "before https://www.falklandsbiographies.org/test-url/biographies/12 after",
            "before https://falklandsbiographies.org/test-url/biographies/12 after",
            "before https://dfb.ukfit.webfactional.com/test-url/biographies/12 after",
            "before http://dfb-staging.ukfit.webfactional.com/test-url/biographies/12 after",
            "before http://0.0.0.0:3000/test-url/biographies/12 after"
            ]
        for test_str in test_strs:
            self.assertEqual(clean_urls(test_str), "before /test-url/biographies/12 after")