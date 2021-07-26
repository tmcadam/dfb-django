from django.core.management.base import BaseCommand, CommandError
from biographies.models import *
import json

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)

    def read_file(self, file_path):
        # Opening JSON file
        with open(file_path,'r') as f:
            return json.load(f)

    def handle(self, *args, **options):
        file_path = options['file_path'][0]
        print(file_path)

        data = self.read_file(file_path)
        length = 0

        if "countries" in data:
            Country.objects.all().delete()
            length = len(data["countries"])
            for country in data["countries"]:
                c = Country(**country)
                c.save()
                print(c.id, c.name)

        if "biographies" in data:
            Biography.objects.all().delete()
            length = len(data["biographies"])
            for biography in data["biographies"]:
                b = Biography(**biography)
                b.save()
                print(b.id, b.title)

        self.stdout.write(self.style.SUCCESS('Successfully loaded {} items'.format(length)))