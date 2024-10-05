from django.test import TestCase, tag
from django.db.models import Value
from django.db.models.functions import Replace

from biographies.models import Biography
from biographies.tests.factories import BiographyFactory

class CleanSlugTests(TestCase):


    @tag("clean_slugs")
    def test_can_create_biography_with_all_fields_present(self):
        bio = BiographyFactory()
        bio.body = """
        <p>FE <a href="/biographies/cobb_frederick">COBB</a>, 
        the Company's young colonial manager 
        William Wickham <a href="/biographies/bertrand_william">BERTRAND</a> and his
        """
        bio.full_clean()
        bio.save()

        Biography.objects.all().update(
            body=Replace('body', 
                         Value(f"biographies/bertrand_william"), 
                         Value(f"biographies/biographies/bertrand_william_new")
                         )
        )

        self.assertEqual(Biography.objects.filter(body__icontains="/biographies/cobb_frederick").count(), 1)
        self.assertEqual(Biography.objects.filter(body__icontains="/biographies/bertrand_william_new").count(), 1)
