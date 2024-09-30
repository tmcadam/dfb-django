
from datetime import datetime as dt

from django.template import RequestContext, Template
from django.test import TestCase, Client, tag

class GlobalContextTests(TestCase):

    @tag("global_context")
    def test_copyright_set_in_context(self):
        client = Client()
        response = client.get("/")
        context = RequestContext(response.request)
        year = str(dt.now().year)[-2:]
        rendered_context = Template("{{ COPYRIGHT }}").render(context=context)
        self.assertEqual(rendered_context, f"2012-{year}")