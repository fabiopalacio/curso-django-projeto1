
import json
from unittest.mock import patch
from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipesHomeApiViewTest(RecipeTestBase):
    def test_home_api_view_func_is_correct(self):
        # Getting the url to recipes:home
        url = reverse('recipes:recipes_api_v1')

        # Getting the view from the url got above
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.home
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewHomeAPI,
            msg="HOME API VIEW - VIEW: The returned view was incorrect.")

    def test_recipes_home_api_view_returns_status_code_200_OK(self):
        # Getting the response to the get recipes:home
        response = self.client.get(reverse('recipes:recipes_api_v1'))

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="HOME API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    def test_recipes_home_api_view_not_loads_templates(self):
        # Getting the response to get recipes:home
        response = self.client.get(reverse('recipes:recipes_api_v1'))

        # Assertions:
        # Check if the template returned to response is the
        # an empty list
        self.assertEqual(
            response.templates,
            [],
            msg="HOME API VIEW - TEMPLATE: Found templates when empty "
            f"list was expected. Found: {response.templates}")

    def test_recipes_home_api_view_loads_only_recipes_published(self):
        # Test to check if unpublished recipes are not sent
        # Created two recipes. The 'Expected' one is the published recipe
        # while the other is not.
        self.make_recipe(title='Expected')
        self.make_recipe(
            is_published=False,
            title='Recipe not published',
            author_data={'username': 'new_author_user'},
            slug='generic-new-slug')

        # Getting the response to the home api view
        response = self.client.get(reverse('recipes:recipes_api_v1'))

        # Converting the response from string to list of dictionaries
        recipes_data = json.loads(response.content.decode('utf-8'))

        # Check if the number of recipes returned is equal to one
        self.assertEqual(
            len(recipes_data),
            1,
            msg="HOME API VIEW - PUBLISHED RECIPES: Found more recipes "
            "than expected."
        )

        # Getting the first item from the list of dictionaries
        recipes_data = recipes_data[0]

        # Checking basic information of the recipe
        # to make sure the published recipe is the one
        # returned from API
        self.assertEqual(
            recipes_data['title'],
            'Expected',
            msg="HOME API VIEW - PUBLISHED RECIPES: Expected title not "
            f"found. Title found: {recipes_data['title']}")

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_home_api_view_paginator_working_correctly(self):
        # Test to check if the paginator is working in the home API view
        # This test uses PER_PAGE value equals to 2, allowing to generate less
        # recipes

        # Creating 3 recipes
        recipes = self.make_recipes_in_batch(3)

        # Getting the first and the last recipes to be used
        # in the assertions. The recipes are ordered by -id, so
        # the first created should be the last displayed
        first_recipe = recipes[0]
        last_recipe = recipes[-1]

        # Getting the response to the home API view
        response = self.client.get(reverse('recipes:recipes_api_v1'))

        # Loading its content as list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Creating  a list with the ids of recipes returned to that page
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if TWO recipes were returned
        self.assertEqual(
            len(data),
            2,
            msg="HOME API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 2. Found: {len(data)}"
        )

        # Check if the last recipe created is returned
        self.assertIn(
            last_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        # Check if the first recipe created is NOT returned
        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Getting the second page to home API view
        response = self.client.get(
            reverse('recipes:recipes_api_v1') + '?page=2')

        # Loading its content as list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Creating  a list with the ids of recipes returned to that page
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if only one recipe was returned
        self.assertEqual(
            len(data),
            1,
            msg="HOME API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 1. Found: {len(data)}"
        )

        # Check if the recipe returned is the first created
        self.assertIn(
            first_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Check if the last recipe created is not in the id_list
        self.assertNotIn(
            last_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        # Getting the response to the third page
        # This page does not exist. So, it should
        # return the first page
        response = self.client.get(
            reverse('recipes:recipes_api_v1') + '?page=3')

        # Loading its content as list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Creating  a list with the ids of recipes returned to that page
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if the returned content is the expected one from the first
        # home API page (same tests)
        self.assertEqual(
            len(data),
            2,
            msg="HOME API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 2. Found: {len(data)}"
        )

        self.assertIn(
            last_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="HOME API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

    def test_recipes_home_api_loads_cover_url(self):
        # Test if the HOME API View loads and adjust cover url
        # This test will change the recipe's cover name and request
        # the HOME API view. The API view should return the JSON content
        # with the cover attribute as a url to the image
        # The EXPECTED URL to images can be defined as:
        # domain/media/image_path/image_name

        # Default domain from django test is 'http://testserver/'
        default_domain = 'http://testserver/'

        # Fictional image name to be used in the test
        image_path = 'images/012345.jpg'

        # Creating a recipe and changing it cover.name to the image_path
        # created above. The Recipe Model create the cover field as a
        # ImageField, so it has the attribute name. Because no file
        # is passed in self.make_recipe(), the name attribute from the
        # cover field is an empty string by default.
        recipe = self.make_recipe()
        recipe.cover.name = image_path
        recipe.save()

        # Requesting HOME API content
        response = self.client.get(
            reverse(
                'recipes:recipes_api_v1'))

        # Converting the response from string to list of dictionaries and
        # getting the first (and only) item from the list
        raw_data = json.loads(response.content)[0]

        # Check if the returned cover has the expected url
        self.assertEqual(
            f'{default_domain}media/{image_path}',
            raw_data['cover'],
            msg="HOME API VIEW - RECIPE'S COVER: Wrong path found. Expected: "
            f"{default_domain}media/{image_path}"
            f"Found: {raw_data['cover']}"
        )


class RecipesCategoryApiViewTest(RecipeTestBase):

    def setUp(self) -> None:
        # SetUp method:
        # Save the path name in the self.path_name
        # Make it easy to adjust in the future
        self.path_name = 'recipes:category_api_v1'
        return super().setUp()

    def test_category_api_view_func_is_correct(self):
        # Getting the url to recipes:category
        url = reverse(self.path_name, kwargs={'category_id': 1})

        # Getting the view from the url got above
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.RecipeListViewCategoryAPI
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewCategoryAPI,
            msg="CATEGORY API VIEW - VIEW: The returned view was incorrect.")

    def test_recipes_category_api_view_returns_status_code_200_OK(self):
        # Require a recipe. If no recipe is found, this view returns 404
        recipe = self.make_recipe()
        # Getting the response to the get category api view
        response = self.client.get(
            reverse(self.path_name, kwargs={'category_id': recipe.category.id}))

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="CATEGORY API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    def test_recipes_category_api_view_returns_code_404_when_no_recipe(self):
        # Getting the response to category API view passing a nonexistent
        # category id
        response = self.client.get(
            reverse(self.path_name, kwargs={'category_id': 1}))

        # Assertions:
        # Checking if the response status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="CATEGORY API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 404. Found {response.status_code}",)

    def test_recipes_category_api_view_not_loads_templates(self):
        # Creating a recipe
        recipe = self.make_recipe()

        # Getting the response to category api view
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'category_id': recipe.category.id}))

        # Assertions:
        # Check if the template returned to response is
        # an empty list
        self.assertEqual(
            response.templates,
            [],
            msg="CATEGORY API VIEW - TEMPLATE: Found templates when empty "
            f"list was expected. Found: {response.templates}")

    def test_recipes_category_api_view_loads_only_recipes_published(self):
        # Test to check if unpublished recipes are not sent through API
        # Creating one published and one not published recipes
        # A category is required, so both recipes can be created under
        # the same category
        category = self.make_category()

        # Creating recipes
        self.make_recipe(title='Expected', category_data=category)
        self.make_recipe(
            is_published=False,
            title='Recipe not published',
            author_data={'username': 'new_author_user'},
            slug='generic-new-slug',
            category_data=category)

        # Getting the response
        response = self.client.get(reverse(self.path_name, kwargs={
                                   'category_id': category.id}))

        # Converting string to list of dict
        recipes_data = json.loads(response.content.decode('utf-8'))

        # Check if only one recipe is returned
        self.assertEqual(
            len(recipes_data),
            1,
            msg="CATEGORY API VIEW - PUBLISHED RECIPES: Found more recipes "
            "than expected."
        )

        # Getting the first item from the list of recipes returned
        recipes_data = recipes_data[0]

        # Check if the recipe returned is the Expected one
        self.assertEqual(
            recipes_data['title'],
            'Expected',
            msg="CATEGORY API VIEW - PUBLISHED RECIPES: Expected title not "
            f"found. Title found: {recipes_data['title']}")

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_category_api_view_paginator_working_correctly(self):
        # Test to check if the paginator is working in the category API view
        # This test uses PER_PAGE value equals to 2, allowing to generate less
        # recipes

        # Creating a category to be used to create new recipes
        category_data = self.make_category()

        # Creating three recipes
        recipes = self.make_recipes_in_batch(3, category_data=category_data)

        # Saving the first and last recipe created to be used in assertions
        first_recipe = recipes[0]
        last_recipe = recipes[-1]

        # Getting the response to the first page of category API view
        response = self.client.get(
            reverse(self.path_name,
                    kwargs={
                        'category_id': first_recipe.category.id}))

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if only two recipes were returned
        self.assertEqual(
            len(data),
            2,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong number of recipes "
            f"returned. Expected: 2. Found: {len(data)}"
        )

        # Check if the last recipe is in the recipes returned
        self.assertIn(
            last_recipe.id,
            id_list,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        # Check if the first recipe created is not in the recipes returned
        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Getting the second page
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'category_id': first_recipe.category.id}
            ) + '?page=2')

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if only one recipe was returned
        self.assertEqual(
            len(data),
            1,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong number of recipes "
            f"returned. Expected: 1. Found: {len(data)}"
        )

        # Check if the first recipe is the one returned
        self.assertIn(
            first_recipe.id,
            id_list,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Getting the third (nonexistent) page. Expected the first page to be returned
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'category_id': first_recipe.category.id}
            ) + '?page=3')

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if two recipes were returned
        self.assertEqual(
            len(data),
            2,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 2. Found: {len(data)}"
        )

        # Check if the last recipe created was returned
        self.assertIn(
            last_recipe.id,
            id_list,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        # Check if the first recipe created is not in the recipes returned
        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="CATEGORY API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

    def test_recipes_category_api_loads_cover_url(self):
        # Test if the CATEGORY API View loads and adjust cover url
        # This test will change the recipe's cover name and request
        # the CATEGORY API view. The API view should return the JSON content
        # with the cover attribute as a url to the image
        # The EXPECTED URL to images can be defined as:
        # domain/media/image_path/image_name

        # Default domain from django test is 'http://testserver/'
        default_domain = 'http://testserver/'

        # Fictional image name to be used in the test
        image_path = 'images/012345.jpg'

        # Creating a recipe and changing it cover.name to the image_path
        # created above. The Recipe Model create the cover field as a
        # ImageField, so it has the attribute name. Because no file
        # is passed in self.make_recipe(), the name attribute from the
        # cover field is an empty string by default.
        recipe = self.make_recipe()
        recipe.cover.name = image_path
        recipe.save()

        # Requesting CATEGORY API content
        response = self.client.get(
            reverse(
                self.path_name, kwargs={'category_id': recipe.category.id}))
        # Converting the response from string to list of dictionaries and
        # getting the first (and only) item from the list
        raw_data = json.loads(response.content)[0]

        # Check if the returned cover has the expected url
        self.assertEqual(
            f'{default_domain}media/{image_path}',
            raw_data['cover'],
            msg="CATEGORY API VIEW - RECIPE'S COVER: Wrong path found. "
            f"Expected: {default_domain}media/{image_path}"
            f"Found: {raw_data['cover']}"
        )


class RecipesSearchApiViewTest(RecipeTestBase):
    def setUp(self) -> None:
        # SetUp method:
        # Save the path name in the self.path_name
        # Make it easy to adjust in the future
        self.path_name = 'recipes:search_api_v1'
        return super().setUp()

    def test_search_api_view_func_is_correct(self):

        # Getting the url to recipes:search_api_v1
        url = reverse(self.path_name)

        # Getting the view from the url got above
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.RecipeListViewSearchAPI
        self.assertIs(
            view.func.view_class,
            views.RecipeListViewSearchAPI,
            msg="SEARCH API VIEW - VIEW: The returned view was incorrect.")

    def test_recipes_search_api_view_returns_status_code_200_OK(self):
        title = 'Just a generic title'

        # Require a recipe. If no recipe is found, this view returns 404
        self.make_recipe(title=title)

        # Getting the response to the get category api view
        response = self.client.get(
            reverse(self.path_name) + f'?q={title}')

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="SEARCH API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    def test_recipes_search_api_view_returns_code_404_when_no_term(self):
        # Getting the response to search category API view passing
        # no search term
        response = self.client.get(
            reverse(self.path_name) + '')

        # Assertions:
        # Checking if the response status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="SEARCH API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 404. Found {response.status_code}",)

    def test_recipes_search_api_view_returns_code_200_when_no_recipe(self):
        # Getting the response to search term without finding
        # any recipe
        response = self.client.get(
            reverse(self.path_name) + '?q=recipe')

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="SEARCH API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    def test_recipes_search_api_view_returns_empty_list_when_no_recipe(self):
        # Getting the response to search API view when no recipe
        # is found
        response = self.client.get(
            reverse(self.path_name) + '?q=recipe')

        # Assertions:
        # Checking if the response content is an empty list
        self.assertEqual(
            response.content.decode('utf-8'),
            '[]',
            msg="SEARCH API VIEW - NO RECIPE: Incorrect return."
            f"Expected: '[]'. Found {response.content.decode('utf-8')}",)

    def test_recipes_search_api_view_not_loads_templates(self):
        self.make_recipe(title='Recipe')

        # Getting the response to search api view
        response = self.client.get(
            reverse(self.path_name) + '?q=recipe')

        # Assertions:
        # Check if the template returned to response is an
        # empty list
        self.assertEqual(
            response.templates,
            [],
            msg="SEARCH API VIEW - TEMPLATE: Found templates when empty "
            f"list was expected. Found: {response.templates}")

    def test_recipes_search_api_view_loads_only_recipes_published(self):
        # Test to check if unpublished recipes are not sent through API
        # Creating one published and one not published recipes

        # Creating recipes
        self.make_recipe(title='Expected')
        self.make_recipe(
            is_published=False,
            title='Recipe not expected',
            author_data={'username': 'new_author_user'},
            slug='generic-new-slug')

        # Getting the response
        response = self.client.get(reverse(self.path_name) + '?q=Expected')

        # Converting string to list of dict
        recipes_data = json.loads(response.content.decode('utf-8'))

        # Check if only one recipe is returned
        self.assertEqual(
            len(recipes_data),
            1,
            msg="SEARCH API VIEW - PUBLISHED RECIPES: Found more recipes "
            "than expected."
        )

        # Getting the first item from the list of recipes returned
        recipes_data = recipes_data[0]

        # Check if the recipe returned is the Expected one
        self.assertEqual(
            recipes_data['title'],
            'Expected',
            msg="SEARCH API VIEW - PUBLISHED RECIPES: Expected title not "
            f"found. Title found: {recipes_data['title']}")

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_search_api_view_paginator_working_correctly(self):
        # Test to check if the paginator is working in the search API view
        # This test uses PER_PAGE value equals to 2, allowing to generate less
        # recipes

        # Creating three recipes
        recipes = self.make_recipes_in_batch(3)

        # Saving the first and last recipe created to be used in assertions
        first_recipe = recipes[0]
        last_recipe = recipes[-1]

        # Getting the response to the first page of category API view
        response = self.client.get(
            reverse(self.path_name) + '?q=recipe')

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if only two recipes were returned
        self.assertEqual(
            len(data),
            2,
            msg="SEARCH API VIEW - PAGINATOR: Wrong number of recipes "
            f"returned. Expected: 2. Found: {len(data)}"
        )

        # Check if the last recipe is in the recipes returned
        self.assertIn(
            last_recipe.id,
            id_list,
            msg="SEARCH API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

    # Check if the first recipe created is not in the recipes returned
        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="SEARCH API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Getting the second page
        response = self.client.get(
            reverse(
                self.path_name) + '?q=recipe&page=2')

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if only one recipe was returned
        self.assertEqual(
            len(data),
            1,
            msg="SEARCH API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 1. Found: {len(data)}"
        )

        # Check if the first recipe is the one returned
        self.assertIn(
            first_recipe.id,
            id_list,
            msg="SEARCH API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

        # Getting the third (nonexistent) page. Expected the first page to be returned
        response = self.client.get(
            reverse(
                self.path_name) + '?q=recipe&page=3')

        # Converting the string to list of dictionaries
        data = json.loads(response.content.decode('utf-8'))

        # Getting the list of recipes' id returned
        id_list = list()
        for recipe in data:
            id_list.append(recipe['id'])

        # Check if two recipes were returned
        self.assertEqual(
            len(data),
            2,
            msg="SEARCH API VIEW - PAGINATOR: Wrong number of recipes returned. "
            f"Expected: 2. Found: {len(data)}"
        )

        # Check if the last recipe created was returned
        self.assertIn(
            last_recipe.id,
            id_list,
            msg="SEARCH API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {last_recipe.id}. Found: {id_list}"
        )

        # Check if the first recipe created is not in the recipes returned
        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg="SEARCH API VIEW - PAGINATOR: Wrong recipes returned. "
            f"Id expected: {first_recipe.id}. Found: {id_list}"
        )

    def test_recipes_search_api_loads_cover_url(self):
        # Test if the SEARCH API View loads and adjust cover url
        # This test will change the recipe's cover name and request
        # the SEARCH API view. The API view should return the JSON content
        # with the cover attribute as a url to the image
        # The EXPECTED URL to images can be defined as:
        # domain/media/image_path/image_name

        # Default domain from django test is 'http://testserver/'
        default_domain = 'http://testserver/'

        # Fictional image name to be used in the test
        image_path = 'images/012345.jpg'

        # Creating a recipe and changing it cover.name to the image_path
        # created above. The Recipe Model create the cover field as a
        # ImageField, so it has the attribute name. Because no file
        # is passed in self.make_recipe(), the name attribute from the
        # cover field is an empty string by default.
        recipe = self.make_recipe()
        recipe.cover.name = image_path
        recipe.save()

        # Requesting SEARCH API content
        response = self.client.get(
            reverse(
                self.path_name) + '?q=recipe')

        # Converting the response from string to list of dictionaries and
        # getting the first (and only) item from the list
        raw_data = json.loads(response.content)[0]

        # Check if the returned cover has the expected url
        self.assertEqual(
            f'{default_domain}media/{image_path}',
            raw_data['cover'],
            msg="SEARCH API VIEW - RECIPE'S COVER: Wrong path found."
            f" Expected: {default_domain}media/{image_path}"
            f"Found: {raw_data['cover']}"
        )


class RecipesDetailApiViewTest(RecipeTestBase):
    def setUp(self) -> None:
        # SetUp method:
        # Save the path name in the self.path_name
        # Make it easy to adjust in the future
        self.path_name = 'recipes:recipe_api_v1'
        return super().setUp()

    def test_recipes_detail_api_view_func_is_correct(self):

        # Getting the url to recipes:category
        url = reverse(self.path_name, kwargs={'pk': 1})

        # Getting the view from the url got above
        view = resolve(url)

        # Assertions:
        # Check if the returned view is views.home
        self.assertIs(
            view.func.view_class,
            views.RecipeDetailAPI,
            msg="DETAIL API VIEW - VIEW: The returned view was incorrect.")

    def test_recipes_detail_api_view_returns_status_code_200_OK(self):
        # Require a recipe. If no recipe is found, this view returns 404
        recipe = self.make_recipe()
        # Getting the response to the get category api view
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': recipe.id}))

        # Assertions:
        # Checking if the response status code is 200
        self.assertEqual(
            response.status_code,
            200,
            msg="DETAIL API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 200. Found {response.status_code}",)

    def test_recipes_detail_api_view_returns_code_404_when_no_recipe(self):
        # Getting the  Detail API view of a nonexistent recipe
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': 1}))

        # Assertions:
        # Checking if the response status code is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="DETAIL API VIEW - STATUS CODE: Incorrect status code."
            f"Expected: 404. Found {response.status_code}",)

    def test_recipes_detail_api_view_not_loads_templates(self):
        recipe = self.make_recipe(title='Recipe')

        # Getting the response to search api view
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': recipe.id}))

        # Assertions:
        # Check if the template returned to response is an empty list
        self.assertEqual(
            response.templates,
            [],
            msg="DETAIL API VIEW - TEMPLATE: Found templates when empty "
            f"list was expected. Found: {response.templates}")

    def test_recipes_detail_api_view_loads_only_recipes_published(self):
        # Test to check if unpublished recipes are not sent through API
        # Creating one not published recipe
        recipe = self.make_recipe(
            is_published=False,
            title='Recipe not published',
            author_data={'username': 'new_author_user'},
            slug='generic-new-slug')

        # Getting the response to the unpublished recipe's id
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': recipe.id}))

        # Check if the status code returned is 404
        self.assertEqual(
            response.status_code,
            404,
            msg="DETAIL API VIEW - PUBLISHED RECIPE: Found unpublished recipe."
        )

    def test_recipes_detail_api_loads_and_returns_tag_list(self):
        # Creating a recipe
        recipe = self.make_recipe(title='Tag list test to DetailApiView')

        # Creating three tags. Two will be add to the created recipe
        tag1 = self.make_tag('FirstTag')
        tag2 = self.make_tag('SecondTag')
        tag3 = self.make_tag('ThirdTag')

        # Adding the tags to the recipe
        recipe.tags.add(tag1, tag2)

        # Getting the response to get the recipe's detailed view
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': recipe.id}))

        # Converting the string to list of dicts
        raw_data = json.loads(response.content)

        # Check if the Recipe title was found to guarantee the
        # recipe returned was the expected
        self.assertEqual(
            recipe.title,
            json.loads(response.content)['title'],
            msg="DETAIL API VIEW - RECIPE'S TITLE: Expected title not found. "
            f"Found: {json.loads(response.content)['title']}"
        )

        # Getting the tags from the recipe
        raw_data = raw_data['tags']

        # Check if the first tag is in the list
        self.assertIn(
            tag1.name,
            raw_data,
            msg="DETAIL API VIEW - RECIPE'S TAG: Expected tag not found. "
            f"Found: {raw_data}"
        )

        # Check if the second tag is in the list
        self.assertIn(
            tag2.name,
            raw_data,
            msg="DETAIL API VIEW - RECIPE'S TAG: Expected tag not found. "
            f"Found: {raw_data}"
        )

        # Check if the third tag is NOT in the list
        self.assertNotIn(
            tag3.name,
            raw_data,
            msg="DETAIL API VIEW - RECIPE'S TAG: Unexpected tag found. "
            f"Found: {raw_data}"
        )

    def test_recipes_detail_api_loads_cover_url(self):
        # Test if the DETAIL API View loads and adjust cover url
        # This test will change the recipe's cover name and request
        # the DETAIL API view. The API view should return the JSON content
        # with the cover attribute as a url to the image
        # The EXPECTED URL to images can be defined as:
        # domain/media/image_path/image_name

        # Default domain from django test is 'http://testserver/'
        default_domain = 'http://testserver/'

        # Fictional image name to be used in the test
        image_path = 'images/012345.jpg'

        # Creating a recipe and changing it cover.name to the image_path
        # created above. The Recipe Model create the cover field as a
        # ImageField, so it has the attribute name. Because no file
        # is passed in self.make_recipe(), the name attribute from the
        # cover field is an empty string by default.
        recipe = self.make_recipe()
        recipe.cover.name = image_path
        recipe.save()

        # Requesting DETAIL API content
        response = self.client.get(
            reverse(self.path_name, kwargs={'pk': recipe.id}))

        # Converting the response from string to list of dictionaries
        raw_data = json.loads(response.content)

        # Check if the returned cover has the expected url
        self.assertEqual(
            f'{default_domain}media/{image_path}',
            raw_data['cover'],
            msg="DETAIL API VIEW - RECIPE'S COVER: Wrong path found. Expected: "
            f"{default_domain}media/{image_path}"
            f"Found: {raw_data['cover']}"
        )
