
import time
from django.test import LiveServerTestCase  # type: ignore
# In case you need static files, use the following Live server:
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_firefox_browser


class RecipeBaseFunctionalTest(LiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_firefox_browser()
        return super().setUp()

    def tearDown(self) -> None:

        self.browser.quit()

        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
