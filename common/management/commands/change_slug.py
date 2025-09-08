from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from django.db.models import Value
from django.db.models import Q

from django.db.models.functions import Replace

from biographies.models import Biography
from images.models import Image
from pages.models import Page


class Command(BaseCommand):
    help = "Update a biography slug and related links in other bios"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("bio_id", type=int)
        parser.add_argument("new_slug", type=str)

        # Named (optional) arguments
        parser.add_argument(
            "--dry_run",
            action="store_true",
            help="Simulate the changes without applying them",
        )

    def handle(self, *args, **options):
        bio = Biography.objects.get(id=options["bio_id"])

        old_slug = bio.slug
        bio.slug = options["new_slug"]

        try:
            bio.full_clean()
            self.stdout.write(self.style.SUCCESS(f"Slug field valid: {bio.slug}"))
        except ValidationError as e:
            print(f"Error changing slug for {bio.title}({bio.id}): {e}")
            raise (e)

        if not options["dry_run"]:
            bio.save()
            self.stdout.write(
                self.style.SUCCESS(f"Slug field updated: {old_slug} -> {bio.slug}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: Slug field would be updated: {old_slug} -> {bio.slug}"
                )
            )

        old_url = f'"/biographies/{old_slug}"'.replace(" ", "%20")
        new_url = f'"/biographies/{bio.slug}"'

        q = (
            Q(body__icontains=old_url)
            | Q(references__icontains=old_url)
            | Q(external_links__icontains=old_url)
        )
        bio_update_count = Biography.objects.filter(q).count()
        image_update_count = Image.objects.filter(caption__icontains=old_url).count()
        pages_update_count = Page.objects.filter(body__icontains=old_url).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Links found: bios({bio_update_count}), images({image_update_count}), pages({pages_update_count})"
            )
        )

        if not options["dry_run"]:
            Biography.objects.all().update(
                body=Replace("body", Value(old_url), Value(new_url)),
                references=Replace("references", Value(old_url), Value(new_url)),
                external_links=Replace(
                    "external_links", Value(old_url), Value(new_url)
                ),
            )
            Image.objects.all().update(
                caption=Replace("caption", Value(old_url), Value(new_url))
            )
            Page.objects.all().update(
                body=Replace("body", Value(old_url), Value(new_url))
            )
            self.stdout.write(
                self.style.SUCCESS(f"Links updated: {old_url} -> {new_url}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: Links would be updated: {old_url} -> {new_url}"
                )
            )
