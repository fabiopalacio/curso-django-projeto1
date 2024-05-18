import time
from django.test import LiveServerTestCase
import pytest
# In case you need static files, use the following Live server:
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_firefox_browser
from selenium.webdriver.common.by import By


class RecipeBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_firefox_browser()
        return super().setUp()

    def tearDown(self) -> None:

        self.browser.quit()

        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    @pytest.mark.slow
    @pytest.mark.functionaltest
    def test_recipe_home_page_without_recipes_display_message(self):

        self.browser.get(self.live_server_url)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipes found here...', body.text)
