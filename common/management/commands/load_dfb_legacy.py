import json
import os

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from biographies.models import Biography, Country
from images.models import Image
from authors.models import Author, BiographyAuthor
from comments.models import Comment
from pages.models import Page


class Command(BaseCommand):
    help = "Cleans DB and loads data from the \
        legacy DFB using a folder of table exports"

    def add_arguments(self, parser):
        parser.add_argument("folder_path", nargs=1, type=str)

    def read_file(self, file_path):
        # Opening JSON file
        with open(file_path, "r") as f:
            return json.load(f)

    def handle(self, *args, **options):
        folder_path = options["folder_path"][0]
        print(f"Loading data from: {folder_path}")

        Biography.objects.all().delete()
        Country.objects.all().delete()
        Author.objects.all().delete()
        BiographyAuthor.objects.all().delete()
        Comment.objects.all().delete()
        Image.objects.all().delete()
        Page.objects.all().delete()

        # read countries
        countries_data = self.read_file(os.path.join(folder_path, "countries.json"))
        length = len(countries_data["countries"])
        for country in countries_data["countries"]:
            Country.objects.create(**country)
        self.stdout.write(
            self.style.SUCCESS("Countries: loaded {} items".format(length))
        )

        # read biograhies
        biographies_data = self.read_file(os.path.join(folder_path, "biographies.json"))
        length = len(biographies_data["biographies"])
        for biography in biographies_data["biographies"]:
            Biography.objects.create(**biography)
        self.stdout.write(
            self.style.SUCCESS("Biographies: loaded {} items".format(length))
        )

        # read authors
        authors_data = self.read_file(os.path.join(folder_path, "authors.json"))
        length = len(authors_data["authors"])
        for author in authors_data["authors"]:
            Author.objects.create(**author)
        self.stdout.write(self.style.SUCCESS("Authors: loaded {} items".format(length)))

        # read biography_authors
        biography_authors_data = self.read_file(
            os.path.join(folder_path, "biography_authors.json")
        )
        length = len(biography_authors_data["biography_authors"])
        for biography_author in biography_authors_data["biography_authors"]:
            # print(biography_author)
            bio = Biography.objects.filter(id=biography_author["biography_id"])
            if bio:
                BiographyAuthor.objects.create(
                    biography=bio[0],
                    author=Author.objects.get(id=biography_author["author_id"]),
                    author_position=biography_author["author_position"],
                    updated_at=biography_author["updated_at"],
                    created_at=biography_author["created_at"],
                )
        self.stdout.write(
            self.style.SUCCESS("BiographyAuthors: loaded {} items".format(length))
        )

        # read comments
        comments_data = self.read_file(os.path.join(folder_path, "_comments_.json"))
        length = len(comments_data["comments"])
        for comment in comments_data["comments"]:
            bio = Biography.objects.filter(id=comment["biography_id"])
            if bio:
                Comment.objects.create(
                    id=comment["id"],
                    biography=bio[0],
                    name=comment["name"],
                    email=comment["email"],
                    comment=comment["comment"],
                    approved=comment["approved"],
                    updated_at=comment["updated_at"],
                    created_at=comment["created_at"],
                )
        self.stdout.write(
            self.style.SUCCESS("Comments: loaded {} items".format(length))
        )

        # read images
        images_data = self.read_file(os.path.join(folder_path, "images.json"))
        length = len(images_data["images"])
        for img in images_data["images"]:
            bio = Biography.objects.filter(id=img["biography_id"])
            image_name = img["image_file_name"].replace(".png", ".jpg")
            Image.objects.create(
                id=img["id"],
                biography=bio[0],
                title=img["title"],
                caption=img["caption"],
                attribution=img["attribution"],
                image=os.path.join("images", image_name),
                updated_at=img["updated_at"],
                created_at=img["created_at"],
            )
        self.stdout.write(self.style.SUCCESS("Images: loaded {} items".format(length)))

        # read pages
        pages_data = self.read_file(os.path.join(folder_path, "static_contents.json"))
        length = len(pages_data["static_contents"])
        for page in pages_data["static_contents"]:
            Page.objects.create(**page)
        self.stdout.write(self.style.SUCCESS("Pages: loaded {} items".format(length)))

        sequence_sql = connection.ops.sequence_reset_sql(
            no_style(),
            [Biography, Country, Author, BiographyAuthor, Comment, Image, Page],
        )
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        self.stdout.write(self.style.SUCCESS("Reset sequences"))
