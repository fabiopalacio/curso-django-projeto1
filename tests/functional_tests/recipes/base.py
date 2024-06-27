
import time
from django.test import LiveServerTestCase  # type: ignore

from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeMixin

from utils.browser import make_firefox_browser

# CLASS Base to Recipes FunctionalTest.
# setup:
#   Create the browser to be used in tests
# tearDown:
#   Quit the browser
# sleep method:
#   Some tests require time to load the page.


class RecipeBaseFunctionalTest(LiveServerTestCase, RecipeMixin):
    # setUp method:
    #   It is called before each test.
    #   It calls the make_firefox_browser() method to create
    #       a browser.
    def setUp(self) -> None:
        self.browser = make_firefox_browser()
        return super().setUp()

    # tearDown method:
    # Quit the browser after each test.
    def tearDown(self) -> None:
        self.browser.quit()

        # Removing recipes from test database after each test
        recipes = Recipe.objects.all()
        recipes.delete()

        return super().tearDown()

    # sleep method:
    # Make it easy to call the time.sleep() method
    def sleep(self, seconds=1):
        time.sleep(seconds)
