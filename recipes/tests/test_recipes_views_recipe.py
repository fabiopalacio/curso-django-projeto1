from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase

# Class to test the Detailed view (recipes:recipe)


class RecipeViewsRecipeTest(RecipeTestBase):

    # TEST if the the correct view is loaded
    def test_recipes_detail_view_function_is_correct(self):
        # Getting the url to the recipes:recipe
        url = reverse('recipes:recipe', kwargs={'id': 1})

        # Getting the view
        view = resolve(url)

        # Assertions:
        # Check if the view returned through the resolve above
        # is the views.recipe
        self.assertIs(
            view.func,
            views.recipe,
            msg="DETAILED VIEW - VIEW: Wrong view returned.")

    # TEST if the recipes:recipe return 404 status code when
    # no recipe was found
    def test_recipes_detail_view_returns_404_if_no_recipe_found(self):
        # Getting the url to a recipe that does NOT exist
        url = reverse('recipes:recipe', kwargs={'id': 98123})
        # Getting the get response to the url
        response = self.client.get(url)

        # Assertions:
        # Check if the response status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="DETAILED VIEW - STATUS CODE: Wrong status code returned. "
            f"Expected: 404. Found: {response.status_code}")

    # TEST if the template shows the recipe
    def test_recipes_detail_load_one_recipe(self):
        # Creating a title to be searched in the assertion
        required_title = 'This is a detail page - It loads one recipe'

        # Creating a recipe with the title above
        self.make_recipe(title=required_title)

        # Saving the response and content
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # Assertionts:
        # Check if the title created above was found in the response HTML
        self.assertIn(
            required_title,
            content,
            msg="DETAILED VIEW - LOADING RECIPE: The view didn't display "
            "the expected title recipe")

    # TEST if the view does NOT show unpublished recipes
    def test_recipes_detail_template_dont_load_not_published_recipes(self):
        # Creating recipe with is_published = False
        recipe = self.make_recipe(is_published=False)

        # Getting the url to recipes:recipe using the above recipe's id
        url = reverse('recipes:recipe', kwargs={'id': recipe.id})

        # Getting the response to the get url
        response = self.client.get(url)

        # Assertions:
        # Check if the status code is 404
        # The recipe is not published, so it should NOT be accessed
        # So, its detailed page should not be available
        # returning the status code 404
        self.assertEqual(
            response.status_code,
            404,
            msg="DETAILED VIEW - UNPUBLISHED RECIPE: Wrong status code. "
            "Unpublished recipe's page did NOT return 404."
            f"Expected: 404. Found: {response.status_code}")
