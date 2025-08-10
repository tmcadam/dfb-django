import factory

from authors.models import Author

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    biography = factory.Sequence(lambda n: 'Biography_%d' % n) 
