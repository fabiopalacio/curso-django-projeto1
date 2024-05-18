from unittest.mock import patch
from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase
# Create your tests here.


class RecipeViewsHomeTest(RecipeTestBase):

    ##########################################################################
    # Home View ('recipes:home')

    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_view_shows_message_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn("No recipes found here...",
                      response.content.decode('utf-8'))

    def test_recipes_home_template_loads_recipes(self):
        category = self.make_category('Café da manhã')
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

# Check if the view found the recipe created above
        self.assertNotIn('Desculpe. Não encontramos nenhuma receita',
                         content)

# Check if the basic information is displayed in the page
        self.assertIn('My Recipe Title', content)
        self.assertIn('Fabio Palacio', content)
        self.assertIn('Recipe Description', content)
        self.assertIn('5 Porções', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('Café da manhã', content)

# Check if the preparation steps is not displayed in the page
        self.assertNotIn('Recipe Preparation Steps', content)

# Check if the placeholer image is insert when no cover image was provided
        self.assertIn('https://via.placeholder.com/1280x720', content)

# Check if the context passed to the view has only one recipe (created above)
        self.assertEqual(len(context), 1)

    def test_recipes_home_template_dont_load_non_published_recipes(self):
        """Recipes with is_published=False are not displayed"""

        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        # Assertions:
        self.assertIn("No recipes found here...", content)

    def test_recipes_home_gets_paginator_numpages_correctly(self):
        for i in range(7):
            self.make_recipe(
                slug=f'recipe-{i}', title='This is one recipe',
                author_data={'username': f'{i}'},
            )

        with patch('recipes.views.PER_PAGE', new=3):
            url = reverse('recipes:home')
            response = self.client.get(url)

            self.assertEqual(
                response.context['recipes'].paginator.num_pages, 3)

            self.assertContains(response, '<div class="recipe-cover">', 3)

            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(1)), 3)
            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(3)), 1)
