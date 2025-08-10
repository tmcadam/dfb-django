from bs4 import BeautifulSoup
from django.test import TestCase, tag
from django.urls import reverse

from authors.models import Author
from .factories import AuthorFactory
from biographies.tests.factories import BiographyFactory

class AuthorViewsTests(TestCase):

    @tag("authors_views")
    def  test_routing_for_authors_index(self):
        url = reverse('authors:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    @tag("authors_views")
    def  test_authors_index_view_returns_all_authors (self):
        for i in range(10):
            AuthorFactory.create()
        response = self.client.get(reverse('authors:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 10)


    @tag("authors_views")
    def  test_authors_index_renders_cards(self):
        for i in range(10):
            AuthorFactory.create()
        response = self.client.get(reverse('authors:index'))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", "card")
        self.assertEqual(len(cards), 10)


    @tag("authors_views")
    def  test_authors_card_has_authors_biographies(self):
        author1 = AuthorFactory.create()
        bio1 = BiographyFactory.create(title="Biography1")
        bio2 = BiographyFactory.create(title="Biography2")
        bio1.authors_connections.add(author1, through_defaults={"author_position":1})
        bio2.authors_connections.add(author1, through_defaults={"author_position":1})

        response = self.client.get(reverse('authors:index'))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        card = soup.find_all("div", "card")[0]
        bios_list = card.find_all("li", "bios-list-item")
        self.assertEqual(len(bios_list), 2)
        self.assertEqual(bios_list[0].a.string, "Biography1")
        self.assertEqual(bios_list[1].a.string, "Biography2")

    @tag("authors_views")
    def  test_authors_card_has_authors_biography_and_other_authors(self):
        author1 = AuthorFactory.create(first_name="Jen", last_name="Author1")
        author2 = AuthorFactory.create(first_name="Bob", last_name="Author2")
        bio1 = BiographyFactory.create(title="Biography1")
        bio1.authors_connections.add(author1, through_defaults={"author_position":1})
        bio1.authors_connections.add(author2, through_defaults={"author_position":2})

        response = self.client.get(reverse('authors:index'))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", "card")
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0].div.h5.string, "Jen Author1")
        bios_list = cards[0].find_all("li", "bios-list-item")
        self.assertEqual(len(bios_list), 1)
        other_authors = bios_list[0].find_all("li", "other-authors-list-item")
        self.assertEqual(len(other_authors), 1)
        self.assertEqual(other_authors[0].span.string.strip(), "Bob Author2")