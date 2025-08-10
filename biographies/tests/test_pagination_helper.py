from unittest import TestCase as SimpleTestCase
from biographies.pagination_helper import generate_pagination_links

from django.test import tag

class PaginationUnitTests(SimpleTestCase):

    @tag("pagination")
    def test_paginator_for_first_page_of_short_list(self):
        links = generate_pagination_links(1,3)

        self.assertEqual(len(links), 5)

        self.assertEqual(links[0].link_type, "curr")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "next")
        self.assertEqual(links[1].link_number, 2)
        self.assertEqual(links[2].link_type, "basic")
        self.assertEqual(links[2].link_number, 3)

        self.assertEqual(links[3].link_type, "nav_next")
        self.assertEqual(links[3].link_number, 2)
        self.assertEqual(links[4].link_type, "nav_last")
        self.assertEqual(links[4].link_number, 3)

    @tag("pagination")
    def test_paginator_for_last_page_of_short_list(self):
        links = generate_pagination_links(3,3)

        self.assertEqual(len(links), 5)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 2)

        self.assertEqual(links[2].link_type, "basic")
        self.assertEqual(links[2].link_number, 1)
        self.assertEqual(links[3].link_type, "prev")
        self.assertEqual(links[3].link_number, 2)
        self.assertEqual(links[4].link_type, "curr")
        self.assertEqual(links[4].link_number, 3)


    @tag("pagination")
    def test_paginator_for_middle_page_of_short_list(self):
        links = generate_pagination_links(2,3)

        self.assertEqual(len(links), 7)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 1)

        self.assertEqual(links[2].link_type, "prev")
        self.assertEqual(links[2].link_number, 1)
        self.assertEqual(links[3].link_type, "curr")
        self.assertEqual(links[3].link_number, 2)
        self.assertEqual(links[4].link_type, "next")
        self.assertEqual(links[4].link_number, 3)

        self.assertEqual(links[5].link_type, "nav_next")
        self.assertEqual(links[5].link_number, 3)
        self.assertEqual(links[6].link_type, "nav_last")
        self.assertEqual(links[6].link_number, 3)




    @tag("pagination")
    def test_paginator_for_first_page_of_long_list(self):
        links = generate_pagination_links(1,11)

        self.assertEqual(len(links), 8)

        self.assertEqual(links[0].link_type, "curr")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "next")
        self.assertEqual(links[1].link_number, 2)
        self.assertEqual(links[2].link_type, "basic")
        self.assertEqual(links[2].link_number, 3)
        self.assertEqual(links[3].link_type, "basic")
        self.assertEqual(links[3].link_number, 4)
        self.assertEqual(links[4].link_type, "basic")
        self.assertEqual(links[4].link_number, 5)

        self.assertEqual(links[5].link_type, "epsilon")
        self.assertEqual(links[5].link_number, None)
        self.assertEqual(links[6].link_type, "nav_next")
        self.assertEqual(links[6].link_number, 2)
        self.assertEqual(links[7].link_type, "nav_last")
        self.assertEqual(links[7].link_number, 11)

    @tag("pagination")
    def test_paginator_for_second_page_of_long_list(self):
        links = generate_pagination_links(2,11)

        self.assertEqual(len(links), 11)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 1)

        self.assertEqual(links[2].link_type, "prev")
        self.assertEqual(links[2].link_number, 1)
        self.assertEqual(links[3].link_type, "curr")
        self.assertEqual(links[3].link_number, 2)
        self.assertEqual(links[4].link_type, "next")
        self.assertEqual(links[4].link_number, 3)
        self.assertEqual(links[5].link_type, "basic")
        self.assertEqual(links[5].link_number, 4)
        self.assertEqual(links[6].link_type, "basic")
        self.assertEqual(links[6].link_number, 5)
        self.assertEqual(links[7].link_type, "basic")
        self.assertEqual(links[7].link_number, 6)

        self.assertEqual(links[8].link_type, "epsilon")
        self.assertEqual(links[8].link_number, None)
        self.assertEqual(links[9].link_type, "nav_next")
        self.assertEqual(links[9].link_number, 3)
        self.assertEqual(links[10].link_type, "nav_last")
        self.assertEqual(links[10].link_number, 11)


    @tag("pagination")
    def test_paginator_for_second_last_page_of_long_list(self):
        links = generate_pagination_links(10,11)

        self.assertEqual(len(links), 11)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 9)
        self.assertEqual(links[2].link_type, "epsilon")
        self.assertEqual(links[2].link_number, None)

        self.assertEqual(links[3].link_type, "basic")
        self.assertEqual(links[3].link_number, 6)
        self.assertEqual(links[4].link_type, "basic")
        self.assertEqual(links[4].link_number, 7)
        self.assertEqual(links[5].link_type, "basic")
        self.assertEqual(links[5].link_number, 8)
        self.assertEqual(links[6].link_type, "prev")
        self.assertEqual(links[6].link_number, 9)
        self.assertEqual(links[7].link_type, "curr")
        self.assertEqual(links[7].link_number, 10)
        self.assertEqual(links[8].link_type, "next")
        self.assertEqual(links[8].link_number, 11)

        self.assertEqual(links[9].link_type, "nav_next")
        self.assertEqual(links[9].link_number, 11)
        self.assertEqual(links[10].link_type, "nav_last")
        self.assertEqual(links[10].link_number, 11)


    @tag("pagination")
    def test_paginator_for_last_page_of_long_list(self):
        links = generate_pagination_links(11,11)

        self.assertEqual(len(links), 8)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 10)
        self.assertEqual(links[2].link_type, "epsilon")
        self.assertEqual(links[2].link_number, None)

        self.assertEqual(links[3].link_type, "basic")
        self.assertEqual(links[3].link_number, 7)
        self.assertEqual(links[4].link_type, "basic")
        self.assertEqual(links[4].link_number, 8)
        self.assertEqual(links[5].link_type, "basic")
        self.assertEqual(links[5].link_number, 9)
        self.assertEqual(links[6].link_type, "prev")
        self.assertEqual(links[6].link_number, 10)
        self.assertEqual(links[7].link_type, "curr")
        self.assertEqual(links[7].link_number, 11)


    @tag("pagination")
    def test_paginator_for_middle_page_of_long_list(self):
        links = generate_pagination_links(6,11)

        self.assertEqual(len(links), 15)

        self.assertEqual(links[0].link_type, "nav_first")
        self.assertEqual(links[0].link_number, 1)
        self.assertEqual(links[1].link_type, "nav_prev")
        self.assertEqual(links[1].link_number, 5)
        self.assertEqual(links[2].link_type, "epsilon")
        self.assertEqual(links[2].link_number, None)

        self.assertEqual(links[3].link_type, "basic")
        self.assertEqual(links[3].link_number, 2)
        self.assertEqual(links[4].link_type, "basic")
        self.assertEqual(links[4].link_number, 3)
        self.assertEqual(links[5].link_type, "basic")
        self.assertEqual(links[5].link_number, 4)
        self.assertEqual(links[6].link_type, "prev")
        self.assertEqual(links[6].link_number, 5)
        self.assertEqual(links[7].link_type, "curr")
        self.assertEqual(links[7].link_number, 6)
        self.assertEqual(links[8].link_type, "next")
        self.assertEqual(links[8].link_number, 7)
        self.assertEqual(links[9].link_type, "basic")
        self.assertEqual(links[9].link_number, 8)
        self.assertEqual(links[10].link_type, "basic")
        self.assertEqual(links[10].link_number, 9)
        self.assertEqual(links[11].link_type, "basic")
        self.assertEqual(links[11].link_number, 10)

        self.assertEqual(links[12].link_type, "epsilon")
        self.assertEqual(links[12].link_number, None)
        self.assertEqual(links[13].link_type, "nav_next")
        self.assertEqual(links[13].link_number, 7)
        self.assertEqual(links[14].link_type, "nav_last")
        self.assertEqual(links[14].link_number, 11)