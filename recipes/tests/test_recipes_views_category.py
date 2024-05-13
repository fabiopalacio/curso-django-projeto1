from unittest.mock import patch
from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase
# Create your tests here.


class RecipeViewsCategoryTest(RecipeTestBase):

    # Category View ('recipes:category')

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 98123}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_template_loads_recipes(self):
        required_title = 'This is a categorical test'

        # Recipe is required
        self.make_recipe(title=required_title)

        # Saving the response and content
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

    # Assertions:
        self.assertIn(required_title, content)

    def test_recipes_category_view_return_404_if_its_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={
                'category_id': recipe.category.id}))

        # Assertions:
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_gets_paginator_numpages_correctly(self):
        category = self.make_category('MyCategory')
        for i in range(7):
            self.make_recipe(
                slug=f'recipe-{i}', title='This is one recipe',
                author_data={'username': f'{i}'},
                category_data=category
            )

        with patch('recipes.views.PER_PAGE', new=3):
            url = reverse('recipes:category', kwargs={'category_id': 1})
            response = self.client.get(url)

            self.assertEqual(
                response.context['recipes'].paginator.num_pages, 3)

            self.assertContains(response, '<div class="recipe-cover">', 3)

            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(1)), 3)
            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(3)), 1)
