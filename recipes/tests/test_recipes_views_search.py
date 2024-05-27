from unittest.mock import patch
from django.urls import resolve, reverse  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase

# CLASS to Search view


class RecipeViewsSearchTest(RecipeTestBase):

    # TEST if the recipes:search is returning the correct view.
    def test_recipes_search_uses_correct_view_function(self):
        # Getting the url to recipes:search
        url = reverse('recipes:search')

        # resolving the url
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.search
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewSearch,
            msg="SEARCH VIEW - VIEW: The returned view was NOT the "
            "expected one")

    # TEST if the recipes:search loads the correct template
    def test_recipes_search_loads_correct_template(self):
        # Getting the response to get the url from (reverse(recipes:search)
        # with a search term = "teste")
        response = self.client.get(reverse('recipes:search') + '?q=teste')

        # Assertions:
        # Check if the template used by the view is the
        # 'recipes/pages/search.html'
        self.assertTemplateUsed(
            response,
            'recipes/pages/search.html',
            msg_prefix="SEARCH VIEW - TEMPLATE: Wrong template used.")

    # TEST if the recipes:search returns 404 when no search term is passed
    def test_recipes_search_raises_404_if_no_search_term(self):
        # Getting the response to get reverse(recipes:search)
        # without a search term)
        response = self.client.get(reverse('recipes:search'))

        # Assertions:
        # Check if the status code returned is 404
        # The view should return 404 when no search term is passed.
        self.assertEqual(
            response.status_code,
            404,
            msg="SEARCH VIEW - NO SEARCH TERM: Wrong status code when "
            "no search term is passed. Expected: 404. Found: "
            f"{response.status_code}")

    # TEST if the search term is in the page AND is escaping special characters
    def test_recipes_search_term_is_in_page_title_and_escaped(self):
        # Getting the response to search for <Teste>.
        # The response should NOT have the characters
        # Only their reoresentation: &lt; &gt; and &quot;
        response = self.client.get(reverse('recipes:search') + '?q=<Teste>')

        # Assertions:
        # Check if the text with escaped characters was found in the HTML
        # The &quot; is used by the view and, because of that, it is not
        # required in the search term to test if the view is escaping the
        # quotes. The assertion search for it.
        self.assertIn(
            'Pesquisando por &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8'),
            msg="SEARCH VIEW - ESCAPING CHARACTERS: The escaped representation"
            " was not found int the response HTML")

        # Check if the text without escaped characters was NOT found in the
        # HTML
        self.assertNotIn(
            'Pesquisando por "<Teste>"',
            response.content.decode('utf-8'),
            msg="SEARCH VIEW - ESCAPING CHARACTERS: The text without escaping "
            "the special characters was found in the HTML")

    # TEST if the recipes:search can find a recipe by title:
    def test_recipes_search_can_find_recipe_by_title(self):

        # Creating two recipes with different titles
        # to be used in cross validation below.
        title1 = 'This is the recipe one'
        title2 = 'This is the recipe two'
        recipe1 = self.make_recipe(
            slug='recipe-one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='recipe-two', title=title2, author_data={'username': 'two'}
        )

        # Getting the url to recipes:search
        search_url = reverse('recipes:search')

        # Getting the response to search each title
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')

        # Getting the response to search a expression that
        # should return both recipes
        responseboth = self.client.get(f'{search_url}?q=this')

        # Assertions
        # RESPONSE1:
        # Check if the recipe1 was found in the response1 context
        self.assertIn(
            recipe1,
            response1.context['recipes'],
            msg='SEARCH VIEW - FINDING TITLE: Expected recipe was not found')

        # Check if the recipe2 was NOT found in the response1 context
        self.assertNotIn(
            recipe2,
            response1.context['recipes'],
            msg='SEARCH VIEW - FINDING TITLE: Unexpected recipe found')

        # RESPONSE2:
        # Check if the recipe2 was found in the response2 context
        self.assertIn(
            recipe2,
            response2.context['recipes'],
            msg='SEARCH VIEW - FINDING TITLE: Expected recipe was not found')

        # Check if the recipe1 was NOT found in the response2 context
        self.assertNotIn(
            recipe1,
            response2.context['recipes'],
            msg='SEARCH VIEW - FINDING TITLE: Unexpected recipe found')

        # RESPONSEBOTH
        # Check if the context length is equal to two (2 recipes found)
        self.assertEqual(
            len(responseboth.context['recipes']),
            2,
            msg="SEARCH VIEW: FINDING TITLE: Unexpected response context "
            "length. Expected: 2. Found: "
            f"{len(responseboth.context['recipes'])}")

        # Check if the recipe 1 is in the responseboth
        self.assertIn(
            recipe1,
            responseboth.context['recipes'],
            msg="SEARCH VIEW - FINDING TITLE: Expected recipe (1) was not "
            "found.")

        # Check if the recipe 2 is in the responseboth
        self.assertIn(
            recipe2,
            responseboth.context['recipes'],
            msg="SEARCH VIEW - FINDING TITLE: Expected recipe (2) was not "
            "found.")

    # TEST if search view can find recipes by description
    def test_recipes_search_can_find_recipe_by_description(self):

        # Creating two recipes with different titles
        # to be used in cross validation below.
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

        # Getting the url to recipes:search
        search_url = reverse('recipes:search')

        # Getting the response to each description
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')

        # Getting the response to search a expression that
        # should return both recipes
        responseboth = self.client.get(f'{search_url}?q=this')

        # Assertions
        # RESPONSE1
        # Check if recipe1 was found in the response1 context
        self.assertIn(
            recipe1,
            response1.context['recipes'],
            msg="SEARCH VIEW - FINDING DESCRIPTION: "
            "Expected recipe was not found")

        # Check if recipe2 was NOT found in the response1 context
        self.assertNotIn(
            recipe2,
            response1.context['recipes'],
            msg="SEARCH VIEW - FINDING DESCRIPTION: "
            "Unexpected recipe found.")

        # RESPONSE2
        # Check if recipe2 was found in the response2 context
        self.assertIn(
            recipe2,
            response2.context['recipes'],
            msg="SEARCH VIEW - FINDING DESCRIPTION: "
            "Expected recipe was not found")
        # Check if recipe1 was NOT found in the response2 context
        self.assertNotIn(
            recipe1,
            response2.context['recipes'],
            msg="SEARCH VIEW - FINDING DESCRIPTION: "
            "Unexpected recipe found.")

        # RESPONSEBOTH
        # Check if the context length is equal to two (2 recipes found)
        self.assertEqual(
            len(responseboth.context['recipes']),
            2,
            msg="SEARCH VIEW: FINDING DESCRIPTION: Unexpected response context"
            " length. Expected: 2. Found: "
            f"{len(responseboth.context['recipes'])}")

        # Check if recipe1 was found in the responseboth context
        self.assertIn(
            recipe1,
            responseboth.context['recipes'],
            msg="SEARCH VIEW - FINDING TITLE: Expected recipe (1) was not "
            "found.")

        # Check if recipe2 was found in the responseboth context
        self.assertIn(
            recipe2,
            responseboth.context['recipes'],
            msg="SEARCH VIEW - FINDING TITLE: Expected recipe (2) was not "
            "found.")

    # TEST if search view gets paginator and numpages correctly
    def test_recipe_search_gets_paginator_numpages_correctly(self):

        # Creating seven recipes
        self.make_recipes_in_batch(qty=7)

        # Using patch to change recipes per page
        # quantity to three
        with patch('recipes.views.PER_PAGE', 3):
            # Getting the url to recipes:search
            search_url = reverse('recipes:search')

            # Getting the response to get the url above
            # searching by 'recipe'
            response = self.client.get(f'{search_url}?q=recipe')

            # Assertions:
            # Check if the context paginator have 3 pages
            self.assertEqual(
                response.context['recipes'].paginator.num_pages,
                3,
                msg="SEARCH VIEW - PAGINATOR: Wrong number of pages. "
                "Expected: 3. Found: "
                f"{response.context['recipes'].paginator.num_pages}")

            # Check if the response has 3 recipes
            # represented by its cover image's div
            self.assertContains(
                response,
                '<div class="recipe-cover">',
                3,
                msg_prefix="SEARCH VIEW - PAGINATOR: The response HTML has "
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
                msg="SEARCH VIEW - PAGINATOR: The first page has the wrong "
                "number of recipes. Expected: 3. Found: "
                f"{len(response.context['recipes'].paginator.get_page(1))}",)

            # Checking the third page
            self.assertEqual(
                len(response.context['recipes'].paginator.get_page(4)),
                1,
                msg="SEARCH VIEW - PAGINATOR: The first page has the wrong "
                "number of recipes. Expected: 1. Found: "
                f"{len(response.context['recipes'].paginator.get_page(3))}",)
