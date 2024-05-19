from unittest.mock import patch
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
