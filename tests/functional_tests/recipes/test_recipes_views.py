import pytest

from unittest.mock import patch
from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest

# pytest mark - mark this class as functionaltest
# allows to control what test to run with pytest


@pytest.mark.functionaltest
# CLASS to test Recipe Pages view. It extends the RecipeBaseFunctionalTest,
# which configures the setup, teardown, and some methods.
# Each test here already has a browser created
class RecipePageFunctionalTest(RecipeBaseFunctionalTest):
    # TEST if home page without recipes display information
    # to the user
    def test_recipes_home_page_without_recipes_display_message(self):
        # Getting to the home page
        self.browser.get(self.live_server_url)

        # Getting the body of the page
        body = self.browser.find_element(By.TAG_NAME, 'body')

        # Assertions:
        # Check if 'No recipes found here...' is in the body
        self.assertIn(
            'No recipes found here...',
            body.text,
            msg="RECIPES_HOME - NO RECIPES FOUND: Info message not displayed."
            "Expected message: No recipes found here...")

    # TEST if home page loads recipes
    # Using patch to change PER_PAGE value
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_home_page_loads_recipes(self):
        # Creating one recipe.
        # Only one is required to not show the info message
        self.make_recipes_in_batch(1)

        # Getting the home page
        self.browser.get(self.live_server_url)

        # Getting the body of the page
        body = self.browser.find_element(By.TAG_NAME, 'body')

        # Checking if the info message is not found in the body
        # Info message not expected:
        #       'No recipes found here...'
        self.assertNotIn(
            'No recipes found here...',
            body.text,
            msg="RECIPES_HOME - NO RECIPES FOUND: Info message found when "
            "it was not expected to. Message: 'No recipes found here...'")

    # TEST if recipes search page show correct recipes
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_search_page_can_find_correct_recipes(self):

        # Creating 7 recipes. Just to have a good amount of recipes
        recipes = self.make_recipes_in_batch(qty=7)

        # Changing the title of one recipe to be search for.
        # The title will be saved in neede_title variable
        needed_title = 'Look for this title'
        # Changing the title of recipes[0]
        recipes[0].title = needed_title
        # Saving the changes
        recipes[0].save()

        # Getting the home page
        self.browser.get(self.live_server_url)

        # Finding the search bar by its XPATH
        input_field = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipe..."]')

        # Finding the search button to be clicked
        search_button = self.browser.find_element(
            By.CLASS_NAME,
            'search-button')

        # Entering the text. The text we are searching for is the
        # recipe title changed above
        input_field.send_keys(needed_title)

        # Pressing the button search
        search_button.click()

        # Wait a while to page load
        self.sleep(1)

        # Assertions:
        # Check if the title searched for was found in the element with
        # recipe class
        self.assertIn(
            needed_title,
            self.browser.find_element(By.CLASS_NAME, 'recipe').text,
            msg="RECIPES SEARCH PAGE - Searched recipe not found."
        )

    # Using patch yo change the value of PER_PAGE to 2
    # Allow to use less recipes and, yet, generate multiple
    # pages, making the test faster
    @patch('recipes.views.PER_PAGE', new=2)
    # TEST if the pagination is working in the home page.
    # It creates 3 recipes. But, becaus patch above changes
    # the value of PER_PAGE to 2, these recipes should be
    # displayed in 2 pages, the first page with 2 recipes
    # and the second one with one recipe
    def test_recipes_home_pagination_is_working(self):
        # Creating recipes
        self.make_recipes_in_batch(qty=3)

        # Getting to the home page:
        # User open the page
        self.browser.get(self.live_server_url)

        # Detect the pagination and select the second page
        page2 = self.browser.find_element(
            By.XPATH,
            "//a[@aria-label='Go to page 2']"
        )

        # Scroll down the page. Required because the test
        # is not using static files, so the element capture above
        # (saved in page2 variable) is not clickable without scrolling
        # down the page
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Clicking the element to go to page 2
        page2.click()

        # Wait a while to page load
        self.sleep(1)

        # Assertions:
        # Check if only one element with class='recipe' was found.
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            1,
            msg="RECIPES HOME - PAGINATION: Expected to find one recipe."
            " Found: "
            f"{len(self.browser.find_elements(By.CLASS_NAME, 'recipe'))}")

    # TEST if recipes search raises 404 when accessed withou
    # a search term.

    def test_recipes_search_page_404_when_no_term(self):
        # Getting to the search page, without passing the search term
        # as an argument
        self.browser.get(self.live_server_url + reverse('recipes:search'))

        # Assertions:
        # Check if
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

    @patch('recipes.views.PER_PAGE', new=1)
    def test_recipes_home_page_adjust_pagination_correctly(self):
        self.make_recipes_in_batch(5)
        self.browser.get(
            self.live_server_url +
            reverse('recipes:home'))

        self.sleep(1)

        pag_container = self.browser.find_element(
            By.CLASS_NAME, 'pagination-content')

        span_field = pag_container.find_element(By.TAG_NAME, 'span')
        self.assertIn(
            '...',
            span_field.text,
            msg="RECIPES_PAGINATION - '...': Span content not found."
        )

        self.assertIn(
            '3 4 ... 5',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="RECIPE_PAGINATION - PAGE NAVIGATION: "
            "Navigation numbers not found."
        )

    @patch('recipes.views.PER_PAGE', new=1)
    def test_recipes_home_page_limit_page(self):
        self.make_recipes_in_batch(5)
        self.browser.get(
            self.live_server_url +
            reverse('recipes:home') + '?page=12')

        self.sleep(1)

        pag_container = self.browser.find_element(
            By.CLASS_NAME, 'pagination-content')

        div_field = pag_container.find_element(By.TAG_NAME, 'div')

        self.assertIn(
            'Current page, page 1',
            div_field.accessible_name,
            msg="RECIPES_PAGINATION - CURRENT PAGE 1': Pagination did not ."
            "redirect to page 1 when page requested is out of range."
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_home_page_page_invalid_redirect_page_1(self):
        self.make_recipes_in_batch(5)
        self.browser.get(
            self.live_server_url +
            reverse('recipes:home') + '?page=text')

        self.sleep(1)

        pag_container = self.browser.find_element(
            By.CLASS_NAME, 'pagination-content')

        div_field = pag_container.find_element(By.TAG_NAME, 'div')

        self.assertIn(
            'Current page, page 1',
            div_field.accessible_name,
            msg="RECIPES_PAGINATION - CURRENT PAGE 1': Pagination did not ."
            "redirect to page 1."
        )


@pytest.mark.functionaltest
class RecipesTagsFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipes_tag_view_return_404_when_no_recipe_found(self):
        self.browser.get(
            self.live_server_url +
            reverse('recipes:tag', kwargs={'tag_name': 'abcde'}))
        self.assertIn(
            'No recipes found here...',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="RECIPES TAG VIEW - NO RECIPE FOUND: Tag view not"
            "expected to find any recipes. Informative message not "
            "found in body."
        )

    def test_recipes_tag_view_loads_recipes(self):
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
