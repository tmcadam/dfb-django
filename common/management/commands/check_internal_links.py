import re

from django.core.management.base import BaseCommand


from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from biographies.models import Biography


class Command(BaseCommand):
    help = "Checks all the internal links in all biographies and produces a report"

    def handle(self, *args, **options):
        updated = 0
        count = Biography.objects.all().count()

        errors = []

        for bio in Biography.objects.all():
            print(f"Bio: {bio.title}")

            links = re.findall(r"<a.*?>.*?</a>", bio.body)
            for link in links:
                print(f"\t{link}")
                url_matches = re.findall(r"\"/biographies/([^/]+)\"", link)
                title = re.findall(r"<a.*?>(.*?)</a>", link)[0].strip()

                if len(url_matches) == 0:
                    # errors.append(f"EXT: Bio:{bio.title}({bio.slug}) Lnk: {title}")
                    continue

                slug = url_matches[0].strip().replace("%20", " ")

                print(f"\t{title} ({slug})")
                try:
                    reverse("biographies:show", args=[slug])
                except NoReverseMatch:
                    errors.append(
                        f"MISS_LNK: Bio:{bio.title}({bio.slug}) Lnk: {title}({slug})"
                    )

                if slug == bio.slug.strip():
                    errors.append(
                        f"SELF_REF: Bio:{bio.title}({bio.slug}) Lnk: {title}({slug})"
                    )

        [print(e) for e in errors]

        self.stdout.write(
            self.style.SUCCESS(f"Slug fields updated: {updated} / {count}")
        )
