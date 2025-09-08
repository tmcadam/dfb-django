from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError


from biographies.models import Biography, Country
from authors.models import Author
from images.models import Image
from comments.models import Comment


class Command(BaseCommand):
    help = "Checks all the objects in the system are valid and produces a report"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--save",
            action="store_true",
            help="Save objects as well",
        )

    def handle(self, *args, **options):
        bio_count = Biography.objects.all().count()
        bio_errors = []
        for bio in Biography.objects.all():
            try:
                bio.full_clean()
                if options["save"]:
                    bio.save()
            except ValidationError as e:
                bio_errors.append(f"Bio: {bio.id} - {e}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Bios checked: {bio_count} Errors found: {len(bio_errors)} Saved: {options['save']}"
            )
        )

        images_count = Image.objects.all().count()
        image_errors = []
        for image in Image.objects.all():
            try:
                image.full_clean()
                if options["save"]:
                    image.save()
            except ValidationError as e:
                image_errors.append(f"Image: {image.id} - {e}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Images checked: {images_count}. Errors found: {len(image_errors)} Saved: {options['save']}"
            )
        )

        authors_count = Author.objects.all().count()
        author_errors = []
        for author in Author.objects.all():
            try:
                author.full_clean()
                if options["save"]:
                    author.save()
            except ValidationError as e:
                author_errors.append(f"Author: {author.id} - {e}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Authors checked: {authors_count}. Errors found: {len(author_errors)} Saved: {options['save']}"
            )
        )

        countries_count = Country.objects.all().count()
        country_errors = []
        for country in Country.objects.all():
            try:
                country.full_clean()
                if options["save"]:
                    country.save()
            except ValidationError as e:
                country_errors.append(f"Country: {country.id} - {e}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Countries checked: {countries_count}. Errors found: {len(country_errors)} Saved: {options['save']}"
            )
        )

        comments_count = Comment.objects.all().count()
        comment_errors = []
        for comment in Comment.objects.all():
            try:
                comment.full_clean()
                if options["save"]:
                    comment.save()
            except ValidationError as e:
                comment_errors.append(f"Comment: {comment.id} - {e}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Comments checked: {comments_count}. Errors found: {len(comment_errors)} Saved: {options['save']}"
            )
        )

        for error in (
            bio_errors + image_errors + author_errors + country_errors + comment_errors
        ):
            self.stdout.write(self.style.ERROR(f"Error found: {error}"))
