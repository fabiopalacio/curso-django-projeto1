from django.urls import resolve, reverse  # type: ignore
from unittest.mock import patch

from recipes import views
from .test_recipe_base import RecipeTestBase

# CLASS to test the Category view


class RecipeViewsCategoryTest(RecipeTestBase):

    # Category View ('recipes:category')

    # TEST if the recipes:category is returning the right view (views.category)
    def test_recipes_category_view_function_is_correct(self):
        # Getting the url from the recipes:category
        url = reverse('recipes:category', kwargs={'category_id': 1})

        # Getting the view from the url
        view = resolve(url)

        # Assertions
        # Checking if the view returned above is the views.category
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewCategory,
            msg="CATEGORY VIEW: The View returned is incorrect")

    # TEST if the category view returns 404 if no recipe was found
    def test_recipes_category_view_returns_404_if_no_recipes_found(self):
        # Getting the url from the recipes:category
        url = reverse('recipes:category', kwargs={'category_id': 98123})

        # Getting the response to the url
        response = self.client.get(url)

        # Assertions:
        # Check if the response's status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="CATEGORY VIEW - 404 STATUS CODE: Status code incorrect."
            f" Expected code: STATUS CODE 404. Found: {response.status_code}",)

    # TEST if the category view loads recipes
    def test_recipes_category_template_loads_recipes(self):
        # Creating a title to a recipe
        required_title = 'This is a categorical test'

        # Creating a recipe with the above title
        self.make_recipe(title=required_title)

        # Saving the response and html content
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

    # Assertions:
    # Checking if the recipe title is displayed in the html content
        self.assertIn(
            required_title,
            content,
            msg="CATEGORY VIEW - LOADING RECIPE: The expected recipe title "
            "was not found in the response HTML.",)

    # TEST to check if the view returns 404 when only recipes with
    # is_published = False exists
    def test_recipes_category_view_return_404_if_its_not_published(self):
        # Creating a new recipe with is_published=False
        recipe = self.make_recipe(is_published=False)
        # Getting the response
        response = self.client.get(
            reverse('recipes:category', kwargs={
                'category_id': recipe.category.id}))

        # Assertions:
        # Checking if the response's status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="CATEGORY VIEW - STATUS 404: Status code is incorrect. "
            f"Expected: 404. Found: {response.status_code}")

    # TEST to check if the category views is callling paginator
    # and getting the correct number of pages
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipes_category_gets_paginator_numpages_correctly(self):
        # Creating a new category. It will be use to all recipes in this test
        category = self.make_category('MyCategory')

        # Creating 7 recipes in the same category
        self.make_recipes_in_batch(qty=7, category_data=category)

        # Using patch to create a new paginator with
        # 3 recipes per page

        # Getting the url to the recipes:category with
        # category_id = 1
        url = reverse('recipes:category', kwargs={'category_id': 1})

        # Getting the response to the url above
        response = self.client.get(url)

        # Assertions:
        # Check if the page has the paginator attribute exists
        # in the response, with num_pages equals to 3
        self.assertEqual(
            response.context['recipes'].paginator.num_pages,
            3,
            msg="CATEGORY VIEW - PAGINATOR: The paginator page got the "
            "wrong number of pages. Expected: 3. "
            f"Found: {response.context['recipes'].paginator.num_pages}",)

        # Check if the response has three recipe's cover
        # Representing the 3 recipes per page
        self.assertContains(
            response,
            '<div class="recipe-cover">',
            3,
            msg_prefix="CATEGORY VIEW - PAGINATOR: The response HTML has "
            "the wrong number of recipes.")

        # Checking if the number of recipes per page is correct.
        # Seven recipes were created.
        # Three recipes are displayed in each page, so:
        # The first and second pages should have three recipes
        # The third page should have one recipe

        # Checking the first page
        self.assertEqual(
            len(response.context['recipes'].paginator.get_page(1)),
            3,
            msg="CATEGORY VIEW - PAGINATOR: The first page has the wrong "
            "number of recipes. Expected: 3. Found: "
            f"{len(response.context['recipes'].paginator.get_page(1))}",)

        # Checking the third page
        self.assertEqual(
            len(response.context['recipes'].paginator.get_page(3)),
            1,
            msg="CATEGORY VIEW - PAGINATOR: The third page has the wrong "
            "number of recipes. Expected: 1. Found: "
            f"{len(response.context['recipes'].paginator.get_page(3))}",)
