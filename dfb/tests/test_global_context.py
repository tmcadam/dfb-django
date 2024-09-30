
from datetime import datetime as dt

from django.template import RequestContext, Template
from django.test import TestCase, tag, override_settings

class GlobalContextTests(TestCase):

    @tag("global_context")
    def test_copyright_set_in_context(self):
        response = self.client.get("/")
        context = RequestContext(response.request)
        year = str(dt.now().year)[-2:]
        rendered_context = Template("{{ COPYRIGHT }}").render(context=context)
        self.assertEqual(rendered_context, f"2012-{year}")

    @tag("global_context")
    @override_settings(ENVIRONMENT="Development")
    def test_environment_page_title(self):
        response = self.client.get("/")
        context = RequestContext(response.request)
        rendered_context = Template("{{ ENVIRONMENT }}").render(context=context)
        self.assertEqual(rendered_context, "Development")