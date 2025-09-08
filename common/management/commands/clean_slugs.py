from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from django.utils.text import slugify
from django.db.models import Value

from django.db.models.functions import Replace

from biographies.models import Biography
from images.models import Image


class Command(BaseCommand):
    help = "Resets featured bios on home page"

    def make_slug(self, bio, word_count=3):
        words = bio.title.split(" ")
        basic_slug = "_".join(words[:word_count])
        return slugify(basic_slug)

    def handle(self, *args, **options):
        updated = 0
        count = Biography.objects.all().count()

        replacements = []

        for bio in Biography.objects.all():
            print(f"\n\nProcessing: {bio.title}")

            old_slug = bio.slug
            bio.slug = self.make_slug(bio, word_count=3)

            # recursively suffix slug until valid
            c = 1

            def check_slug(c):
                try:
                    bio.full_clean()
                except ValidationError:
                    if c == 1:
                        bio.slug += f"_{c}"
                    else:
                        bio.slug = bio.slug[:-2] + f"_{c}"
                    c += 1
                    check_slug(c)
                return

            check_slug(c)

            bio.save()

            print(f"Old Slug: {old_slug} / New Slug: {bio.slug}")

            if old_slug == bio.slug:
                print("Slugs are the same. Nothing to update")
                continue
            else:
                updated += 1
                old_url = f'"/biographies/{old_slug}"'.replace(" ", "%20")
                new_url = f'"/biographies/{bio.slug}"'

                print("Slug updated. Updating biography and images fields")
                print(f"Replacing {old_url} with {new_url}")
                replacements.append((old_url, new_url))

        print("Running replacements queries")
        for r in replacements:
            Biography.objects.all().update(
                body=Replace("body", Value(r[0]), Value(r[1])),
                references=Replace("references", Value(r[0]), Value(r[1])),
                external_links=Replace("external_links", Value(r[0]), Value(r[1])),
            )
            Image.objects.all().update(
                caption=Replace("caption", Value(r[0]), Value(r[1]))
            )

        self.stdout.write(
            self.style.SUCCESS(f"Slug fields updated: {updated} / {count}")
        )
