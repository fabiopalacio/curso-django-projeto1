from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

# CLASS to test Recipes URLs


class RecipesURLsTest(TestCase):

    # TEST to check if the url from "recipes:home" is "/"
    def test_recipes_home_url_is_correct(self):
        # Getting the url through reverse() method
        url = reverse('recipes:home')
        # Checking if the recipes:home url is '/'
        self.assertEqual(
            url,
            '/',
            msg=f"RECIPES URLS - HOME PAGE: Expected: '/'. Found: {url}",)

    # TEST to check the url to the category page
    def test_recipes_category_url_is_correct(self):
        # Getting the url to the category page with category_id = 1
        url = reverse('recipes:category', kwargs={'category_id': 1})

        # Checking if the returned url is /recipes/category/category_id/
        self.assertEqual(
            url,
            '/recipes/category/1/',
            msg="RECIPES URLS - CATEGORY PAGE: "
            f"Expected: '/recipes/category/1/'. Found: {url}",)

    # TEST to check the url to the details page
    def test_recipes_detail_url_is_correct(self):
        # Getting the url to the details page with recipe id = 1
        url = reverse('recipes:recipe', kwargs={'pk': 1})

        # Checking if the returned url is /recipes/id/
        self.assertEqual(
            url,
            '/recipes/1/',
            msg="RECIPES URLS - DETAILS PAGE: "
            f"Expected: '/recipes/1/'. Found: {url}")

    # TEST to check the url to the search page
    def test_recipes_search_url_is_correct(self):
        # Getting the url to the search page

        url = reverse('recipes:search')

        # Checking if the url returned is /recipes/search/
        self.assertEqual(
            url,
            '/recipes/search/',
            msg="RECIPES URLS - SEARCH PAGE: Expected: "
            f"'/recipes/search/'. Found: {url}",)

    # TEST to check the url to the tag page
    def test_recipes_tag_url_is_correct(self):
        # Getting the url to the tag page

        url = reverse('recipes:tag', kwargs={'tag_name': 'name'})

        # Checking if the url returned is /recipes/search/
        self.assertEqual(
            url,
            '/recipes/tag/name/',
            msg="RECIPES URLS - TAG PAGE: Expected: "
            f"'/recipes/tag/'. Found: {url}",)
