from unittest import TestCase
from unittest.mock import patch

from django.http import HttpRequest
import pytest  # type: ignore


from recipes.tests.test_recipe_base import RecipeMixin
from utils.pagination import make_pagination_range, make_pagination


@pytest.mark.django_db
class PaginationTest(TestCase, RecipeMixin):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # Current page = 1
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_pagination_middle_ranges_are_correct(self):

        # Current page = 10
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual(pagination[1], 10)
        # Current page = 12
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual(pagination[1], 12)

    def test_make_pagination_stop_range_less_or_equal_total_pages(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_make_pagination_current_page_1_when_ValueError(self):
        recipes = self.make_recipes_in_batch(20)
        request = HttpRequest()
        request.method = 'GET'
        request.GET['page'] = '4'
        page_obj, pagination = make_pagination(
            request=request, per_page=1, qty_pages=4, queryset=recipes)
        self.assertEqual(
            pagination['current_page'], 4,
            msg='Failed to convert: int("int")')

        request = HttpRequest()
        request.method = 'GET'
        request.GET['page'] = 'anyText'
        page_obj, pagination = make_pagination(
            request=request, per_page=4, qty_pages=4, queryset='')
        self.assertEqual(
            pagination['current_page'], 1,
            msg='Failed in the try block: did not change the current page to one when failed to convert the page query to int')  # noqa: E501

        request.GET['page'] = '84'
        page_obj, pagination = make_pagination(
            request=request, per_page=9, qty_pages=4, queryset=recipes)
        self.assertEqual(
            pagination['current_page'], 1,
            msg='PAGINATION: Failed to get page 1 when out of range page '
            'was requested.')
