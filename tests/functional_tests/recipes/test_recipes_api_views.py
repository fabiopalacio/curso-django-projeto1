from unittest.mock import patch
from selenium.webdriver.common.by import By
from django.urls import reverse
import pytest
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
import json


@pytest.mark.functionaltest
class RecipeHomeApiView(RecipeBaseFunctionalTest):
    # Class to test Home Api View

    def test_home_api_returns_json_content(self):
        recipe = self.make_recipe()
        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipes_api_v1'))
        self.sleep(2)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs-API_HOME: Dictionary lenght unexpected. Expected 1. '
            f'Found {len(raw_data)}'
        )

        raw_data = raw_data[0]

        self.assertEqual(
            len(raw_data),
            18,
            msg='RECIPEs-API_HOME: Dictionary lenght unexpected. Expected 18. '
            f'Found {len(raw_data)}'
        )

        self.assertEqual(
            recipe.id,
            raw_data['id'],
            msg='RECIPEs-API_HOME: RECIPE ID. Wrong id found. '
            f'Expeted: \"{recipe.id}\". '
            f'Found {raw_data["id"]}'
        )

        self.assertEqual(
            'My Recipe Title',
            raw_data['title'],
            msg='RECIPEs-API_HOME: RECIPE TITLE. Wrong recipe title found. '
            'Expeted: "My Recipe Title". '
            f'Found {raw_data["title"]}'
        )

        self.assertEqual(
            'Recipe Description',
            raw_data['description'],
            msg='RECIPEs-API_HOME: RECIPE DESCRIPTION. Wrong recipe'
            ' description found. Expeted: "Recipe description". '
            f'Found {raw_data["description"]}'
        )

        self.assertEqual(
            'recipe-slug',
            raw_data['slug'],
            msg='RECIPEs-API_HOME: RECIPE SLUG. Wrong recipe slug found. '
            'Expeted: "recipe-slug". '
            f'Found {raw_data["slug"]}'
        )

        self.assertEqual(
            10,
            raw_data['preparation_time'],
            msg='RECIPEs-API_HOME: RECIPE PPEPARATION TIME. Wrong preparation'
            ' time found. Expeted: "10". '
            f'Found {raw_data["preparation_time"]}'
        )

        self.assertEqual(
            'minutes',
            raw_data['preparation_time_unit'],
            msg='RECIPEs-API_HOME: RECIPE PPEPARATION TIME. Wrong preparation '
            'time unit found. Expeted: "10". '
            f'Found {raw_data["preparation_time_unit"]}'
        )

        self.assertEqual(
            5,
            raw_data['servings'],
            msg='RECIPEs-API_HOME: RECIPE SERVINGS. Wrong servings found. '
            'Expeted: "5". '
            f'Found {raw_data["servings"]}'
        )

        self.assertEqual(
            'portions',
            raw_data['servings_unit'],
            msg='RECIPEs-API_HOME: RECIPE SERVINGS. Wrong servings unit found.'
            ' Expeted: "Porções". '
            f'Found {raw_data["servings_unit"]}'
        )

        self.assertEqual(
            "Recipe Preparation Steps",
            raw_data['preparation_steps'],
            msg='RECIPEs-API_HOME: RECIPE PREPARATION STEPS. Wrong preparation'
            ' steps found. Expeted: "Recipe Preparation Steps". '
            f'Found {raw_data["preparation_steps"]}'
        )

        self.assertEqual(
            False,
            raw_data['preparation_steps_is_html'],
            msg='RECIPEs-API_HOME: RECIPE PREPARATION STEPS. Wrong preparation'
            ' steps is html value found. Expeted: "False". '
            f'Found {raw_data["preparation_steps_is_html"]}'
        )

        self.assertEqual(
            True,
            raw_data['is_published'],
            msg='RECIPEs-API_HOME: RECIPE IS PUBLISHED. Wrong is published'
            ' value found. Expeted: "True". '
            f'Found {raw_data["is_published"]}'
        )

        self.assertEqual(
            '',
            raw_data['cover'],
            msg='RECIPEs-API_HOME: RECIPE COVER. Wrong cover url'
            ' found. Expeted: "". '
            f'Found {raw_data["cover"]}'
        )

        self.assertEqual(
            recipe.author_id,
            raw_data['author_id'],
            msg='RECIPEs-API_HOME: RECIPE AUTHOR. Wrong author id '
            'found. Expeted: "1". '
            f'Found {raw_data["author_id"]}'
        )

        self.assertEqual(
            'Joe Smith',
            raw_data['author_name'],
            msg='RECIPEs-API_HOME: RECIPE AUTHOR. Wrong author name '
            'found. Expeted: "Joe Smith". '
            f'Found {raw_data["author_name"]}'
        )

        self.assertEqual(
            recipe.category_id,
            raw_data['category_id'],
            msg='RECIPEs-API_HOME: RECIPE CATEGORY. Wrong category id '
            f'found. Expeted: "{recipe.category_id}". '
            f'Found {raw_data["category_id"]}'
        )

        self.assertEqual(
            'Default Category',
            raw_data['category_name'],
            msg='RECIPEs-API_HOME: RECIPE CATEGORY. Wrong category name '
            'found. Expeted: "Default Category". '
            f'Found {raw_data["category_name"]}'
        )

        self.assertEqual(
            '',
            raw_data['tags'],
            msg='RECIPEs-API_HOME: RECIPE TITLE. Wrong tags list found. '
            'Expeted: Empty string. '
            f'Found {raw_data["tags"]}'
        )

    def test_home_api_returns_empty_list_when_no_recipe(self):
        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipes_api_v1'))
        self.sleep(2)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            len(raw_data),
            0,
            msg='RECIPEs-API_HOME: Dictionary lenght unexpected. Expected 0. '
            f'Found {len(raw_data)}'
        )

        self.assertEqual(
            [],
            raw_data,
            msg='RECIPEs-API_HOME: RECIPE TITLE. Wrong tags list found. '
            'Expeted: Empty list. '
            f'Found {raw_data}'
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_home_api_pagination_works(self):
        recipes = self.make_recipes_in_batch(3)
        first_recipe_id = recipes[0].id
        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipes_api_v1'))
        self.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe_id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id not Expected: "{first_recipe_id}". '
            f'Ids Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipes_api_v1') + '?page=2')

        self.sleep(2)

        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 1. Found: {len(raw_data)}.'
        )

        self.assertIn(
            first_recipe_id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id Expected: "{first_recipe_id}". '
            f'Id(s) Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipes_api_v1') + '?page=3')

        self.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes in page 3. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe_id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes in page 3. Id not Expected: "{first_recipe_id}". '
            f'Ids Found: "{id_list}".'
        )


@pytest.mark.functionaltest
class RecipeCategoryApiView(RecipeBaseFunctionalTest):
    # Class to test Category Api View

    def test_category_api_returns_json_content(self):
        recipe = self.make_recipe()
        category_id = recipe.category_id
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:category_api_v1',
                kwargs={'category_id': category_id}))
        self.sleep(3)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs - API_CATEGORY: Dictionary lenght unexpected. '
            f'Expected 1. '
            f'Found {len(raw_data)}'
        )

        raw_data = raw_data[0]

        self.assertEqual(
            len(raw_data),
            18,
            msg='RECIPEs - API_CATEGORY: Dictionary lenght unexpected. '
            f'Expected 18. Found {len(raw_data)}'
        )

        self.assertEqual(
            recipe.id,
            raw_data['id'],
            msg='RECIPEs - API_CATEGORY: RECIPE ID. Wrong id found. '
            f'Expeted: "{recipe.id}". '
            f'Found {raw_data["id"]}'
        )

        self.assertEqual(
            'My Recipe Title',
            raw_data['title'],
            msg='RECIPEs - API_CATEGORY: RECIPE TITLE. Wrong recipe title'
            ' found. Expeted: "My Recipe Title". '
            f'Found {raw_data["title"]}'
        )

        self.assertEqual(
            'Recipe Description',
            raw_data['description'],
            msg='RECIPEs - API_CATEGORY: RECIPE DESCRIPTION. Wrong recipe '
            'description found. Expeted: "Recipe description". '
            f'Found {raw_data["description"]}'
        )

        self.assertEqual(
            'recipe-slug',
            raw_data['slug'],
            msg='RECIPEs - API_CATEGORY: RECIPE SLUG. Wrong recipe slug found.'
            ' Expeted: "recipe-slug". '
            f'Found {raw_data["slug"]}'
        )

        self.assertEqual(
            10,
            raw_data['preparation_time'],
            msg='RECIPEs - API_CATEGORY: RECIPE PPEPARATION TIME. '
            'Wrong preparation time found. Expeted: "10". '
            f'Found {raw_data["preparation_time"]}'
        )

        self.assertEqual(
            'minutes',
            raw_data['preparation_time_unit'],
            msg='RECIPEs - API_CATEGORY: RECIPE PPEPARATION TIME. Wrong'
            ' preparation time unit found. Expeted: "10". '
            f'Found {raw_data["preparation_time_unit"]}'
        )

        self.assertEqual(
            5,
            raw_data['servings'],
            msg='RECIPEs - API_CATEGORY: RECIPE SERVINGS. Wrong servings'
            ' found. Expeted: "5". '
            f'Found {raw_data["servings"]}'
        )

        self.assertEqual(
            'portions',
            raw_data['servings_unit'],
            msg='RECIPEs - API_CATEGORY: RECIPE SERVINGS. Wrong servings '
            'unit found. Expeted: "Porções". '
            f'Found {raw_data["servings_unit"]}'
        )

        self.assertEqual(
            "Recipe Preparation Steps",
            raw_data['preparation_steps'],
            msg='RECIPEs - API_CATEGORY: RECIPE PREPARATION STEPS. Wrong'
            ' preparation steps found. Expeted: "Recipe Preparation Steps". '
            f'Found {raw_data["preparation_steps"]}'
        )

        self.assertEqual(
            False,
            raw_data['preparation_steps_is_html'],
            msg='RECIPEs - API_CATEGORY: RECIPE PREPARATION STEPS. Wrong'
            ' preparation steps is html value found. Expeted: "False". '
            f'Found {raw_data["preparation_steps_is_html"]}'
        )

        self.assertEqual(
            True,
            raw_data['is_published'],
            msg='RECIPEs - API_CATEGORY: RECIPE IS PUBLISHED. Wrong is'
            ' published value found. Expeted: "True". '
            f'Found {raw_data["is_published"]}'
        )

        self.assertEqual(
            '',
            raw_data['cover'],
            msg='RECIPEs - API_CATEGORY: RECIPE COVER. Wrong cover url'
            ' found. Expeted: "". '
            f'Found {raw_data["cover"]}'
        )

        self.assertEqual(
            recipe.author_id,
            raw_data['author_id'],
            msg='RECIPEs - API_CATEGORY: RECIPE AUTHOR. Wrong author id '
            'found. Expeted: "1". '
            f'Found {raw_data["author_id"]}'
        )

        self.assertEqual(
            'Joe Smith',
            raw_data['author_name'],
            msg='RECIPEs - API_CATEGORY: RECIPE AUTHOR. Wrong author name '
            'found. Expeted: "Joe Smith". '
            f'Found {raw_data["author_name"]}'
        )

        self.assertEqual(
            category_id,
            raw_data['category_id'],
            msg='RECIPEs - API_CATEGORY: RECIPE CATEGORY. Wrong category id '
            f'found. Expeted: "{recipe.category_id}". '
            f'Found {raw_data["category_id"]}'
        )

        self.assertEqual(
            'Default Category',
            raw_data['category_name'],
            msg='RECIPEs - API_CATEGORY: RECIPE CATEGORY. Wrong category name '
            'found. Expeted: "Default Category". '
            f'Found {raw_data["category_name"]}'
        )

        self.assertEqual(
            '',
            raw_data['tags'],
            msg='RECIPEs - API_CATEGORY: RECIPE TITLE. Wrong tags list found. '
            'Expeted: Empty string. '
            f'Found {raw_data["tags"]}'
        )

    def test_category_api_returns_empty_list_when_no_recipe(self):
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:category_api_v1',
                kwargs={'category_id': 1}))
        self.sleep(3)

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn(
            'Not Found',
            body,
            msg='RECIPES-CATEGORY: Wrong category did not return 404. '
            'Expected message: "Not Found". '
            f'Found {body}'
        )

    def test_category_api_returns_only_desired_recipes(self):
        first_category = self.make_category(name='First category')
        second_category = self.make_category(name='Second category')

        number_of_recipes = 3

        self.make_recipes_in_batch(
            qty=number_of_recipes, category_data=first_category)
        self.make_recipe(category_data=second_category)

        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:category_api_v1',
                kwargs={'category_id': first_category.id}))
        self.sleep(3)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = self.browser.find_element(By.TAG_NAME, 'pre').text
        self.assertNotIn(
            second_category.name,
            raw_data,
            msg='RECIPES-CATEGORY: JSON returned unexpected '
            f'recipes. Not expected to found: "{second_category.name}". '
            f'Raw data found: {raw_data}'
        )

        self.assertNotIn(
            second_category.name,
            raw_data,
            msg='RECIPES-CATEGORY: JSON returned unexpected '
            f'recipes. Not expected to found: "{second_category.name}". '
            f'Raw data found: {raw_data}'
        )
        raw_data = json.loads(raw_data)

        self.assertEqual(
            number_of_recipes,
            len(raw_data),
            msg='RECIPES-CATEGORY: JSON returned unexpected quantity of '
            f'recipes. Expected: "{number_of_recipes}". '
            f'Found {len(raw_data)}'
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_category_api_pagination_works(self):

        category = self.make_category(name='First category')

        recipes = self.make_recipes_in_batch(
            qty=3, category_data=category)

        first_recipe = recipes[0]

        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:category_api_v1',
                kwargs={'category_id': category.id}))

        self.sleep(2)

        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id not Expected: "{first_recipe.id}". '
            f'Ids Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:category_api_v1',
                    kwargs={'category_id': category.id}) + '?page=2')

        self.sleep(2)

        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 1. Found: {len(raw_data)}.'
        )

        self.assertIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id Expected: "{first_recipe.id}". '
            f'Id(s) Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:category_api_v1',
                    kwargs={'category_id': category.id}) + '?page=3')

        self.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes in page 3. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes in page 3. Id not Expected: "{first_recipe.id}". '
            f'Ids Found: "{id_list}".'
        )


@pytest.mark.functionaltest
class RecipeSearchApiView(RecipeBaseFunctionalTest):
    # Class to test Search Api View

    def test_search_api_returns_correct_json(self):
        recipe = self.make_recipe(title='ThisOne')

        self.make_recipes_in_batch()
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:search_api_v1') + '?q=ThisOne')
        self.sleep(2)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs - API_SEARCH: Dictionary lenght unexpected. '
            f'Expected 1. '
            f'Found {len(raw_data)}'
        )

        raw_data = raw_data[0]

        self.assertEqual(
            len(raw_data),
            18,
            msg='RECIPEs - API_SEARCH: Dictionary lenght unexpected. '
            f'Expected 18. Found {len(raw_data)}'
        )

        self.assertEqual(
            recipe.title,
            raw_data['title'],
            msg='RECIPEs - API_SEARCH: RECIPE TITLE. Wrong recipe found. '
            f'Expeted title: "{recipe.title}". '
            f'Found {raw_data["title"]}'
        )

    def test_search_api_returns_empty_list_when_no_recipe(self):
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:search_api_v1') + '?q=justAText')
        self.sleep(2)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            [],
            raw_data,
            msg='RECIPES-CATEGORY: JSON returned unexpected. '
            f'Expected: []. '
            f'Found {raw_data}'
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_search_api_pagination_works(self):

        recipes = self.make_recipes_in_batch(qty=3)
        first_recipe = recipes[0]

        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:search_api_v1') + '?q=recipe')

        self.sleep(2)

        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id not Expected: "{first_recipe.id}". '
            f'Ids Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:search_api_v1') + '?q=recipe&page=2')

        self.sleep(2)

        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            1,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes. Expected: 1. Found: {len(raw_data)}.'
        )

        self.assertIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes. Id Expected: "{first_recipe.id}". '
            f'Id(s) Found: "{id_list}".'
        )

        self.browser.get(
            self.live_server_url +
            reverse('recipes:search_api_v1') + '?q=recipe&page=3')

        self.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="rawdata-tab"]').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        id_list = list()
        for recipe in raw_data:
            id_list.append(recipe['id'])

        self.assertEqual(
            len(raw_data),
            2,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong number of '
            f'recipes in page 3. Expected: 2. Found: {len(raw_data)}.'
        )

        self.assertNotIn(
            first_recipe.id,
            id_list,
            msg='RECIPEs - API_HOME: PAGINATION returned wrong list of '
            f'recipes in page 3. Id not Expected: "{first_recipe.id}". '
            f'Ids Found: "{id_list}".'
        )


@pytest.mark.functionaltest
class RecipeDetailApiView(RecipeBaseFunctionalTest):
    # Class to test Search Api View

    def test_detail_api_returns_correct_json(self):
        recipe = self.make_recipe(title='ThisOne')

        self.make_recipes_in_batch()
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:recipe_api_v1', kwargs={'pk': recipe.id}))
        self.sleep(3)

        self.browser.find_element(By.ID, 'rawdata-tab').click()

        raw_data = json.loads(
            self.browser.find_element(By.TAG_NAME, 'pre').text)

        self.assertEqual(
            18,
            len(raw_data),

            msg='RECIPEs - API_DETAIL: Dictionary lenght unexpected. '
            f'Expected 18. '
            f'Found {len(raw_data)}'
        )

        self.assertEqual(
            recipe.title,
            raw_data['title'],
            msg='RECIPEs - API_DETAIL: RECIPE TITLE. Wrong recipe found. '
            f'Expeted title: "{recipe.title}". '
            f'Found {raw_data["title"]}'
        )

    def test_detail_api_returns_404_when_id_not_found(self):

        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:recipe_api_v1', kwargs={'pk': 124}))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="RECIPEs - API_DETAIL: RECIPE ID. Id not found did "
            "not return 404."
        )
