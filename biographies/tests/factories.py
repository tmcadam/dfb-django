import factory

from biographies.models import Biography, Country

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Sequence(lambda n: 'Country_%d' % n) 

class BiographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biography

    title = factory.Sequence(lambda n: 'Biography_%d' % n) 
    slug = factory.Sequence(lambda n: 'slug-%d' % n) 
    lifespan = factory.Faker('year')
    body = factory.Faker('paragraph')
    authors = factory.Faker('name')
    revisions = factory.Faker('paragraph')
    external_links = factory.Faker('paragraph')
    references = factory.Faker('paragraph')
    primary_country = factory.SubFactory(CountryFactory)
    secondary_country = None
    south_georgia = factory.Faker('pybool')
    featured= factory.Faker('pybool')
