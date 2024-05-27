from unittest.mock import patch
from django.urls import reverse
import pytest

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By


@pytest.mark.slow
@pytest.mark.functionaltest
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipes_home_page_without_recipes_display_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here...', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_home_page_loads_recipes(self):
        self.make_recipes_in_batch(3)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertNotIn('No recipes found here...', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_search_page_can_find_correct_recipes(self):
        recipes = self.make_recipes_in_batch(qty=7)

        needed_title = 'Look for this title'
        recipes[0].title = needed_title
        recipes[0].save()

        # Simulating user opening the page
        self.browser.get(self.live_server_url)

        # Finding the search bar
        input_field = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipe..."]')

        # Finding the search button
        search_button = self.browser.find_element(
            By.CLASS_NAME,
            'search-button')

        # Entering the text
        input_field.send_keys(needed_title)

        # Pressing the button search
        search_button.click()

        self.assertIn(
            needed_title,
            self.browser.find_element(By.CLASS_NAME, 'recipe').text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_home_(self):
        # Creating recipes
        self.make_recipes_in_batch(qty=3)

        # Simulating user's behaviour:
        # User open the page
        self.browser.get(self.live_server_url)

        # Detect the pagination and select the second page
        page2 = self.browser.find_element(
            By.XPATH,
            "//a[@aria-label='Go to page 2']"
        )

        # Scroll down the page
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Click
        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 1)

    def test_recipes_search_page_404_when_no_term(self):
        self.browser.get(self.live_server_url + reverse('recipes:search'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="SEARCH_VIEW - NO TERM: Search view with no search "
            "term did NOT return Not Found page. Message not found."
        )

    def test_recipes_recipe_return_404_when_wrong_id(self):
        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipe', kwargs={'pk': 1923}))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="SEARCH_VIEW - NO RECIPE: Search view with no search "
            "term did NOT return Not Found page. Message not found."
        )

    def test_recipes_recipe_return_detailed_info(self):

        recipe = self.make_recipe()
        recipe.title = 'The new Recipe Title'
        recipe.full_clean()
        recipe.save()
        self.browser.get(
            self.live_server_url +
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))

        self.assertIn(
            'The new Recipe Title',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="RECIPES_RECIPE - LOAD RECIPE: The view did NOT loaded the "
            "recipe. Recipe title wasn't found in the HTML"
        )

    def test_recipes_category_return_404_when_no_recipe_found(self):
        self.browser.get(
            self.live_server_url +
            reverse('recipes:category', kwargs={'category_id': 12}))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="CATEGORY_VIEW - NO RECIPE FOUND: Category view with was not "
            "expected to find any recipes and return 404. Unexpected recipe "
            "found."
        )

    def test_recipes_category_page_loads_recipes(self):
        category = self.make_category('TestCategory')
        recipe = self.make_recipe(category_data=category)

        self.browser.get(
            self.live_server_url +
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.pk}))

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertNotIn(
            'No recipes found here...',
            body)
        self.assertIn(
            'My Recipe Title',
            body,
            msg="RECIPES_CATEGORY - LOADING RECIPES: Category View did NOT "
            "found expected recipes. Recipe Title not found in the HTML body."
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_category_page_uses_pagination_correctly(self):
        category = self.make_category('TestCategory')
        recipes = self.make_recipes_in_batch(5, category)
        self.browser.get(
            self.live_server_url +
            reverse(
                'recipes:category',
                kwargs={'category_id': recipes[0].category_id}))

        self.sleep(1)

        try:
            element = self.browser.find_element(
                By.XPATH,
                '//a[@aria-label = "Go to page 2"]')
        except Exception:
            element = None

        self.assertNotEqual(
            element,
            None,
            msg="RECIPES_CATEGORY_VIEW - PAGINATION: Link to page 2 not found."
        )
