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
