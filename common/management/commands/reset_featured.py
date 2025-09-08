from django.core.management.base import BaseCommand

from biographies.featured_helper import reset_featured_bios


class Command(BaseCommand):
    help = "Resets featured bios on home page"

    def handle(self, *args, **options):
        bios = reset_featured_bios()

        self.stdout.write(self.style.SUCCESS("Featured bios reset"))
        for bio in bios:
            self.stdout.write(self.style.SUCCESS(f"\t{bio}"))
