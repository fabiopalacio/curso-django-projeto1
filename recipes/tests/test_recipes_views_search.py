from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase
# Create your tests here.


class RecipeViewsSearchTest(RecipeTestBase):

    # Search view

    def test_recipes_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipes_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipes_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipes_search_term_is_in_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<Teste>')
        self.assertIn('Pesquisando por &quot;&lt;Teste&gt;&quot;',
                      response.content.decode('utf-8'))
        self.assertNotIn('Pesquisando por "<Teste>"',
                         response.content.decode('utf-8'))

    def test_recipes_search_can_find_recipe_by_title(self):
        title1 = 'This is the recipe one'
        title2 = 'This is the recipe two'
        recipe1 = self.make_recipe(
            slug='recipe-one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='recipe-two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        responseboth = self.client.get(f'{search_url}?q=this')

        # Assertions
        self.assertIn(recipe1, response1.context['recipes'],
                      msg='The view did not return the correct QuerySet')
        self.assertNotIn(recipe2, response1.context['recipes'],
                         msg='The view did not return the correct QuerySet')

        self.assertIn(recipe2, response2.context['recipes'],
                      msg='The view did not return the correct QuerySet')
        self.assertNotIn(recipe1, response2.context['recipes'],
                         msg='The view did not return the correct QuerySet')

        self.assertEqual(len(responseboth.context['recipes']), 2,
                         msg=f'The QuerySet length expected was 2, but found {len(responseboth.context["recipes"])}')  # noqa: E501

        self.assertIn(recipe1, responseboth.context['recipes'],
                      msg="The first recipe was not found in the QuerySet")
        self.assertIn(recipe2, responseboth.context['recipes'],
                      msg="The second recipe was not found in the QuerySet")

    def test_recipes_search_can_find_recipe_by_description(self):
        description1 = 'This is the recipe one'
        description2 = 'This is the recipe two'
        recipe1 = self.make_recipe(
            slug='recipe-one',
            description=description1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='recipe-two',
            description=description2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')
        responseboth = self.client.get(f'{search_url}?q=this')

        # Assertions
        self.assertIn(recipe1, response1.context['recipes'],
                      msg='The view did not return the correct QuerySet')
        self.assertNotIn(recipe2, response1.context['recipes'],
                         msg='The view did not return the correct QuerySet')

        self.assertIn(recipe2, response2.context['recipes'],
                      msg='The view did not return the correct QuerySet')
        self.assertNotIn(recipe1, response2.context['recipes'],
                         msg='The view did not return the correct QuerySet')

        self.assertEqual(len(responseboth.context['recipes']), 2,
                         msg=f'The QuerySet length expected = 2, found = {len(responseboth.context["recipes"])}')  # noqa: E501

        self.assertIn(recipe1, responseboth.context['recipes'],
                      msg="The first recipe was not found in the QuerySet")
        self.assertIn(recipe2, responseboth.context['recipes'],
                      msg="The second recipe was not found in the QuerySet")

    def test_recipe_search_pagination_displays_nine_items_per_page(self):
        for i in range(10):
            self.make_recipe(
                slug=f'recipe-{i}', title='This is one recipe',
                author_data={'username': f'{i}'},
            )

        search_url = reverse('recipes:search')
        response = self.client.get(f'{search_url}?q=recipe')

        self.assertContains(response, '<div class="recipe-cover">', 9)
