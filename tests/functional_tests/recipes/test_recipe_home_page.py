from unittest.mock import patch
import pytest

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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

    def test_recipes_search_page_can_find_correct_recipes(self):
        recipes = self.make_recipes_in_batch(qty=7)

        needed_title = 'Look for this title'
        recipes[0].title = needed_title
        recipes[0].save()

        self.browser.get(self.live_server_url)

        input_field = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipe..."]')

        input_field.send_keys(needed_title)
        input_field.send_keys(Keys.ENTER)

        # sleep to allow the page to load correctly the search results
        self.sleep(2)

        self.assertIn(
            needed_title,
            self.browser.find_element(By.CLASS_NAME, 'recipe-list-item').text,
        )
