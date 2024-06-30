from unittest.mock import patch
from django.urls import resolve, reverse  # type: ignore

from recipes import views
from .test_recipe_base import RecipeTestBase
# Create your tests here.

# CLASS to test the Home view (recipes:home)


class RecipeViewsHomeTest(RecipeTestBase):

    # TEST if the correct view is being returned:
    def test_recipes_home_view_function_is_correct(self):
        # Getting the url to recipes:home
        url = reverse('recipes:home')

        # Getting the view from the url got above
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.home
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewHome,
            msg="HOME VIEW - VIEW: The returned view was incorrect.")

    # TEST if the home view is returning status code 200
    def test_recipes_home_view_returns_status_code_200_OK(self):
        # Getting the response to the get recipes:home
        response = self.client.get(reverse('recipes:home'))

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="HOME VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    # TEST if the home view is loading the correct template
    def test_recipes_home_view_loads_correct_template(self):
        # Getting the response to get recipes:home
        response = self.client.get(reverse('recipes:home'))

        # Assertions:
        # Check if the template returned to response is the
        # recipes/pages/home.html file
        self.assertTemplateUsed(
            response,
            'recipes/pages/home.html',
            msg_prefix="HOME VIEW - TEMPLATE: Wrong template used.")

    # TEST if the home view shows message when no recipe was found
    def test_recipes_home_view_shows_message_if_no_recipes(self):
        # Getting the response to get recipes:home
        # The message should be displayed in this response
        # because no recipe was registered.
        response = self.client.get(reverse('recipes:home'))

        # Assertions:
        # Check if the "No recipes found here..." message was
        # found in the response html
        self.assertIn(
            "No recipes found here...",
            response.content.decode('utf-8'),
            msg="HOME VIEW - NO RECIPE MESSAGE: The info message was not found"
            " in the response html",)

    # TEST if the home view can load recipes
    def test_recipes_home_template_loads_recipes(self):
        # Creating a category to used with make_recipe() method
        category = self.make_category('Café da manhã')

        # Creating a recipe
        self.make_recipe(
            author_data={
                'first_name': 'Fabio',
                'last_name': 'Palacio'},
            category_data=category,
            title='My Recipe Title',
            description='Recipe Description',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções')

        # Saving the response, content and context
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']

        # Assertions:
        # Check if the view found the recipe created above.
        # If it does not found the recipe, the info message should be found and
        # the test will fail.
        self.assertNotIn(
            'No recipes found here...',
            content,
            msg="HOME VIEW - LOADING RECIPE: The view didn't find a recipe and"
            " presented the 'No recipes found here...' message.")

        # Check if the basic information is displayed in the page
        self.assertIn(
            'My Recipe Title',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe title was NOT found in the"
            " response HTML",)

        self.assertIn(
            'Fabio Palacio',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe author was NOT found in"
            " the response HTML",)

        self.assertIn(
            'Recipe Description',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe description was NOT"
            " found in the response HTML",
        )

        self.assertIn(
            '5 Porções',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe servings was NOT found in"
            " the response HTML",)

        self.assertIn(
            '10 Minutos',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe prep time was NOT found in"
            " the response HTML",)

        self.assertIn(
            'Café da manhã',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe category was NOT found in"
            " the response HTML",)

        # Check if the preparation steps is not displayed in the page
        # This value is displayed only in the detailed view (recipes:recipe)
        self.assertNotIn(
            'Recipe Preparation Steps',
            content,
            msg="HOME VIEW - LOADING RECIPE: Recipe preparation steps WAS "
            "found in the response HTML, but wasn't expected to.",)

        # Check if the placeholer image is insert when no cover image was
        # provided
        self.assertIn(
            'https://via.placeholder.com/1280x720',
            content,
            msg="HOME VIEW - LOADING RECIPE: Default cover image link not "
            "found in response HTML",)

        # Check if the context passed to the view has only one recipe
        # (created above)
        self.assertEqual(
            len(context),
            1,
            msg="HOME VIEW - LOADING RECIPE: The view has wrong number of "
            f"recipes. Expected: 1. Found: {len(context)}")

    # TEST if the home view does not load unpublished recipes
    def test_recipes_home_template_dont_load_not_published_recipes(self):

        # Creating a new recipe with is_published = False
        self.make_recipe(is_published=False)

        # Getting the response to get recipes:home
        response = self.client.get(reverse('recipes:home'))
        # Getting the html content
        content = response.content.decode('utf-8')

        # Assertions:
        # Check if the info message is NOT found in the content
        self.assertIn(
            "No recipes found here...",
            content,
            msg="HOME VIEW - UNPUBLISHED RECIPES: The view didn't show the "
            "sinfo message 'No recipes found here...' when it was "
            "expected to.")

    # TEST if the home view gets the paginator correctly
    def test_recipes_home_gets_paginator_numpages_correctly(self):
        # Creating 7 recipes:
        self.make_recipes_in_batch(qty=7)

        # Using patch to change the paginator configuration
        # to show 3 recipes per page
        with patch('recipes.views.PER_PAGE', new=3):
            # Getting the url to the view
            url = reverse('recipes:home')
            # Getting the response to the above url
            response = self.client.get(url)

            # Assertions:
            # Check if the response context paginator has 3 pages
            self.assertEqual(
                response.context['recipes'].paginator.num_pages,
                3,
                msg="HOME VIEW - PAGINATOR: The response context has wrong "
                "number of pages. Expected: 3. "
                f"Found: {response.context['recipes'].paginator.num_pages,}")

            # Check if the response has the right number of
            # recipes (represented by their cover image's div)
            self.assertContains(
                response,
                '<div class="recipe-cover">',
                3,
                msg_prefix="HOME VIEW - PAGINATOR: The response HTML has "
                "the wrong number of recipes."
            )

            # Checking if the number of recipes per page is correct.
            # Seven recipes were created.
            # Three recipes are displayed in each page, so:
            # The first and second pages should have three recipes
            # The third page should have one recipe

            # Checking the first page:
            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(1)),
                3,
                msg="HOME VIEW - PAGINATOR: The first page has the wrong "
                "number of recipes. Expected: 3. Found: "
                f"{len(response.context['recipes'].paginator.get_page(1))}",)

            # Checking the third page:
            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(3)),
                1,
                msg="HOME VIEW - PAGINATOR: The first page has the wrong "
                "number of recipes. Expected: 1. Found: "
                f"{len(response.context['recipes'].paginator.get_page(3))}",)
