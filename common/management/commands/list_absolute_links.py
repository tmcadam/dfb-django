from django.core.management.base import BaseCommand

from biographies.models import Biography
from images.models import Image

from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = (
        "Checks all the absolute links in all biographies and images and produces a report. "
        "It doesn't check if the links are valid, just if they are absolute. It also doesn't "
        "check the links in the external_links field of biographies."
    )

    def handle(self, *args, **options):
        self.stdout.write("\n\nChecking Biographies")
        self.stdout.write("--------------------")
        for bio in Biography.objects.all():
            links = []
            soup = BeautifulSoup(bio.body or "", "html.parser")
            links += soup.find_all("a")
            soup = BeautifulSoup(bio.references or "", "html.parser")
            links += soup.find_all("a")
            soup = BeautifulSoup(bio.revisions or "", "html.parser")
            links += soup.find_all("a")

            for link in links:
                link_url = link.get("href", "").strip()
                if link_url.startswith("http"):
                    print(f"{link_url}")

        self.stdout.write("\n\nChecking Images")
        self.stdout.write("--------------------")
        for img in Image.objects.all():
            soup = BeautifulSoup(img.caption or "", "html.parser")
            links = soup.find_all("a")
            for link in links:
                link_url = link.get("href", "").strip()
                if link_url.startswith("http"):
                    print(f"{link_url}")

        self.stdout.write(self.style.SUCCESS("\nFinished checking external links\n"))
