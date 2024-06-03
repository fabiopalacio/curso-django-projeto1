import pytest

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium.webdriver.common.by import By

from tests.functional_tests.authors.base_dashboard import DashboardBaseTest

# pytest mark - mark this class as functionaltest
# allows to control what test to run with pytest


@pytest.mark.functionaltest
# CLASS to test DashboardList view. It extends the DashboardBaseTest,
# which configures the setup, teardown, and some methods.
# Each test here already has an user created in and a browser
# The self.login() method opens the login page and insert the user
# data. After the login() method, the webbrowser is in dashboard list page
class DashboardListFunctionalTest(DashboardBaseTest):

    # TEST if the view is loading only unpublished recipes
    def test_dashboardlist_loads_unpublished_recipes_only(self):

        # Creating two recipes unpublished and one published.
        # All 3 with the same author (my_user)
        # We expect to find only 2 recipes in the dashboard list
        self.make_recipe(slug='recipe-1', author=self.my_user)
        self.make_recipe(slug='recipe-2', author=self.my_user)
        self.make_recipe(
            slug='recipe-3',
            author=self.my_user,
            is_published=True)

        # Login with my_user
        self.login()

        # wait a while to page to load
        self.sleep(1)

        # Finding the div which holds the recipes as <li>
        dashboard_list_container = self.browser.find_element(
            By.CLASS_NAME, 'authors-dashboard-container')

        # Finding all recipes. Each one will be an element
        # in li_elements list.
        li_elements = dashboard_list_container.find_elements(
            By.CLASS_NAME, 'authors-dashboard-list-item')

        # Assertions:
        # Check if the list of li elements returned has length == 2
        # (2 unpublished recipes)
        self.assertEqual(
            len(li_elements),
            2,
            msg='DASHBOARD_LIST - RECIPE LIST: Wrong number of li elements '
            'found.'
        )

    # TEST if the dashboardlist view loads only the users' recipes
    # To do so, it creates a second user to be passed as author of
    # one recipe. The other recipe will be the my_user user

    def test_dashboardlist_loads_only_users_recipes(self):
        # Creating a new user
        new_user = User.objects.create_user(
            username='another_user', password='another_password')

        # Creating a new recipe for my_user
        self.make_recipe(slug='recipe-1', author=self.my_user)

        # Creating a new recipe for another_user
        self.make_recipe(slug='recipe-2', author=new_user)

        # Login with my_user
        self.login()

        # wait a while to page to load
        self.sleep(1)

        # Finding the div which holds the recipes as <li>
        dashboard_list_container = self.browser.find_element(
            By.CLASS_NAME, 'authors-dashboard-container')

        # Finding all recipes. Each one will be an element
        # in li_elements list.
        li_elements = dashboard_list_container.find_elements(
            By.CLASS_NAME, 'authors-dashboard-list-item')

        # Assertions:
        # Check if the list of li elements returned has length == 1
        # (1 unpublished my_user's recipe)
        self.assertEqual(
            len(li_elements),
            1,
            msg='DASHBOARD_LIST - RECIPE USER LIST: Wrong number of li '
            "elements found. Probably loaded another user's recipes."
        )

# pytest mark - mark this class as functionaltest
# allows to control what test to run with pytest


@pytest.mark.functionaltest
# CLASS to test the delete recipe button. It extends the DashboardBaseTest,
# which configures the setup, teardown, and some methods.
# Each test here already has an user created in and a browser
# The self.login() method opens the login page and insert the user
# data. After the login() method, the webbrowser is in dashboard list page
class DashboardDeleteRecipeTest(DashboardBaseTest):
    # TEST if the delete button removes the right recipe
    def test_delete_recipe_removes_recipe(self):

        # Creating 2 recipes with different titles to make it easy to
        # differenttiate them
        self.make_recipe(slug='slug-1', author=self.my_user, title='To keep')
        self.make_recipe(slug='slug-2', author=self.my_user, title='To delete')

        # my_user login
        self.login()
        # Wait a while to page to load
        self.sleep(1)

        # Finding the delete buttons by the class name of their symbol.
        delete_buttons = self.browser.find_elements(By.CLASS_NAME, 'fa-xmark')

        # Assertion:
        # Check if it was found 2 delete buttons at this moment
        self.assertEqual(
            len(delete_buttons),
            2,
            msg="DASHBOARD_DELETE_RECIPE - DELETE BUTTONS: Wrong number of "
            f"buttons found. Found: {len(delete_buttons)}"
        )

        # Check if the first recipe (title = 'To keep') was found
        self.assertIn(
            'To keep',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="DASHBOARD_DELETE_RECIPE - DELETE RECIPE: Recipe title not "
            "found. Expected: 'To keep'"
        )

        # Check if the first recipe (title = 'To delete') was found
        self.assertIn(
            'To delete',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="DASHBOARD_DELETE_RECIPE - DELETE RECIPE: Recipe title "
            "not found. Expected: 'To delete'"
        )

        # Clicking in the second recipe delete button, removing it from
        # the list.
        delete_buttons[1].click()

        # Finding the delete buttons by the class name of their symbol.
        delete_buttons = self.browser.find_elements(By.CLASS_NAME, 'fa-xmark')

        # Assertion:
        # Check if it was found 1 delete buttons at this moment
        self.assertEqual(
            len(delete_buttons),
            1,
            msg="DASHBOARD_DELETE_RECIPE - DELETE BUTTONS: Wrong number of "
            f"buttons found. Found: {len(delete_buttons)}"
        )

        # Check if the first recipe (title = 'To keep') was found
        self.assertIn(
            'To keep',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="DASHBOARD_DELETE_RECIPE - DELETE RECIPE: Wrong recipe title "
            "found. Expected: 'To keep'"
        )
        # Check if the first recipe (title = 'To delete') was NOT found
        self.assertNotIn(
            'To delete',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="DASHBOARD_DELETE_RECIPE - DELETE RECIPE: Wrong recipe title "
            "found. Expected: 'To keep'"
        )
