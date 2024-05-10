from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase
# Create your tests here.


class RecipeViewsRecipeTest(RecipeTestBase):

    # Detail view ('recipes:recipe')

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 98123}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_template_load_one_recipe(self):
        required_title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=required_title)

        # Saving the response and content
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # Assertionts:
        self.assertIn(required_title, content)

    def test_recipes_detail_template_dont_load_not_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        # Assertions:
        self.assertEqual(response.status_code, 404)
