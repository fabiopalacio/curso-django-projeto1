from django.test import TestCase  # type: ignore
from django.urls import resolve, reverse  # type: ignore
from recipes import views
from recipes.models import Category, Recipe
from django.contrib.auth.models import User  # type: ignore
# Create your tests here.


class RecipeViewsTest(TestCase):

    ##########################################################################
    # Home View ('recipes:home')

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_shows_message_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('Desculpe. Não encontramos nenhuma receita',
                      response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='FirstCategory')
        author = User.objects.create_user(
            first_name='Joe', last_name='Smith', email='joe_smith@server.com',
            password='123456', username='joeSmith')
        recipe = Recipe.objects.create(  # noqa: F841
            category=category, author=author,
            title='My Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )

# Saving the response, content and context
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']

# Chekc if the view found the recipe created above
        self.assertNotIn('Desculpe. Não encontramos nenhuma receita',
                         content)

# Check if the basic information is displayed in the page
        self.assertIn('My Recipe Title', content)
        self.assertIn('Recipe Description', content)
        self.assertIn('5 Porções', content)
        self.assertIn('10 Minutos', content)

# Check if the preparation steps is not displayed in the page
        self.assertNotIn('Recipe Preparation Steps', content)

# Check if the placeholer image is insert when no cover image was provided
        self.assertIn('https://via.placeholder.com/1280x720', content)

# Check if the context passed to the view has only one recipe (created above)
        self.assertEqual(len(context), 1)

    # Category View ('recipes:category')

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 98123}))
        self.assertEqual(response.status_code, 404)

    # Detail view ('recipes:recipe')
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 98123}))
        self.assertEqual(response.status_code, 404)
