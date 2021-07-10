import factory

from biographies.models import *

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
    name = factory.Faker('country')

class BiographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biography

    title = factory.Faker('name')
    slug = factory.Faker('slug')
    body = factory.Faker('paragraphs', nb=6)
    authors = factory.Faker('name')
    revisions = factory.Faker('paragraph')
    external_links = factory.Faker('paragraph')
    references = factory.Faker('paragraph')
    primary_country = factory.SubFactory(CountryFactory)
    secondary_country= factory.SubFactory(CountryFactory)
    south_georgia = factory.Faker('pybool')
    featured= factory.Faker('pybool')