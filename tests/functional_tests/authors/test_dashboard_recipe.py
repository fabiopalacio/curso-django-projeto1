
from django.urls import reverse
from tests.functional_tests.authors.base_dashboard import DashboardBaseTest
from selenium.webdriver.common.by import By

import pytest

# pytest mark - mark this class as functionaltest
# allows to control what test to run with pytest


@pytest.mark.functionaltest
# CLASS to test DashboardRecipe view. It extends the DashboardBaseTest,
# which configures the setup, teardown, and some methods.
# Each test here already has an user created in and a browser
# The self.login() method opens the login page and insert the user
# data. After the login() method, the webbrowser is in dashboard list page.
# This view is responsible to edit unpublished recipes.
class DashboardRecipeTest(DashboardBaseTest):
    # TEST if the view loads the recipe data
    def test_dashboard_recipe_loads_recipe_data(self):
        # Creating a recipe to my_user
        recipe = self.make_recipe(slug='a-slug', author=self.my_user)

        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Getting the authors:dashboard_recipe view, passing the recipe id
        # allowing the form to recover the recipe data from the database
        self.browser.get(
            self.live_server_url +
            reverse('authors:dashboard_recipe', kwargs={'id': recipe.id}))

        # Wait a while to page load
        self.sleep(1)

        # Getting the recipe form by its class ('main-form')
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        # Getting the form fields by their IDs.
        title_field = form.find_element(By.ID, 'id_title')
        description_field = form.find_element(By.ID, 'id_description')
        preparation_time_field = form.find_element(
            By.ID, 'id_preparation_time')
        servings_field = form.find_element(By.ID, 'id_servings')
        textarea_field = form.find_element(By.ID, 'id_preparation_steps')

        # Assertions:
        # Check if each input field has the expected text in the
        # value attribute
        # Check if the textarea text attribute has the expected value

        # Title assertion
        self.assertEqual(
            'MyNewRecipe',
            title_field.get_attribute('value'),
            msg="DASHBOARD_RECIPE - EDITING RECIPE: Expected title value not "
            "found. Expected: 'MyNewRecipe'. "
            f"Found: {title_field.get_attribute('value')}"
        )

        # Description assertion
        self.assertEqual(
            'description 2',
            description_field.get_attribute('value'),
            msg="DASHBOARD_RECIPE - EDITING RECIPE: Expected description value"
            " not found. Expected: 'description 2'. "
            f"Found: {description_field.get_attribute('value')}"
        )

        # Preparation time assertion
        self.assertEqual(
            '2',
            preparation_time_field.get_attribute('value'),
            msg="DASHBOARD_RECIPE - EDITING RECIPE: Expected preparation time "
            "value not found. Expected: '2'. Found: "
            f"{ preparation_time_field.get_attribute('value')}"
        )

        # Servings assertion
        self.assertEqual(
            '4',
            servings_field.get_attribute('value'),
            msg="DASHBOARD_RECIPE - EDITING RECIPE: Expected servings value"
            " not found. Expected: '4'. Found: "
            f"{servings_field.get_attribute('value')}"
        )

        # Preparation time assertion
        self.assertEqual(
            'preparation_steps',
            textarea_field.text,
            msg="DASHBOARD_RECIPE - EDITING RECIPE: Expected Preparation steps"
            " value not found. Expected: 'preparation_steps'. Found: "
            f"{textarea_field.text}"
        )

    # TEST if the dashboard recipe view raises 404 when an
    # out of range id is requested.
    def test_dashboard_recipe_raises_404_wrong_id(self):
        # Creating a recipe only to have something to be displayed if
        # the page behavior changes at some point.
        recipe = self.make_recipe(slug='a-slug', author=self.my_user)

        # my_user login()
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Getting the dashboard_recipe page passing an out of range id
        # Because there is only one recipe, saved in 'recipe' variable,
        # created above, the last id should be the 'recipe.id' value.
        # So, it is expect to get 404 when a higher id is requested to
        # the form
        self.browser.get(
            self.live_server_url +
            reverse('authors:dashboard_recipe', kwargs={'id': recipe.id+1}))

        # Wait a while to page load
        self.sleep(1)

        # Assertions:
        # Check if 'Not Found' text was found in the body response
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="DASHBOARD_RECIPE - 404: Invalid ID didn't raise 404 error."
        )

# pytest mark - mark this class as functionaltest
# allows to control what test to run with pytest


@pytest.mark.functionaltest
# CLASS to test Dashboard_New_Recipe view. It extends the DashboardBaseTest,
# which configures the setup, teardown, and some methods.
# Each test here already has an user created in and a browser
# The self.login() method opens the login page and insert the user
# data. After the login() method, the webbrowser is in dashboard list page.
# This view is responsible to add new unpublished recipes.
class DashboardNewRecipeTest(DashboardBaseTest):
    # TEST if the view opens a blank form
    def test_dashboard_new_recipe_opens_blank_form(self):

        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()
        # Wait a while to page load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        # Getting the input fields
        #   title, description, preparation_time, and servings
        input_fields = form.find_elements(By.TAG_NAME, 'input')
        # Getting the textarea field
        #   preparation_steps
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # The input fields have same structure, so the assertions will
        # be done inside this for loop.
        for field in input_fields:
            # Checking if the field's id has 'id' in it.
            # Required to jump the hidden input (csrf token)
            if 'id' in field.get_attribute('id'):
                # Assertions:
                # Check if field's attribute 'value' is an empty string
                self.assertEqual(
                    '',
                    field.get_attribute('value'),
                    msg="DASHBOARD_NEW_RECIPE: Expected blank input not found."
                    f"Found: '{field.get_attribute('value')}'"
                )
        # Check if the textarea.text is an empty string
        self.assertEqual(
            '',
            text_area_field.text,
            msg="DASHBOARD_NEW_RECIPE: Expected blank textarea not found."
            f"Found: '{text_area_field.text}'"
        )

    # TEST if the dashboard_new_recipe can save a recipe
    def test_dashboard_new_recipe_saves_recipe(self):

        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()
        # Waiting a while to page load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the inputs and textarea fields
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Using send_keys() to add valid values to each field
        title_input.send_keys('MyRecipeTitle')
        description_input.send_keys('The recipe description')
        preparation_time_input.send_keys('12')
        servings_input.send_keys('2')
        text_area_field.send_keys('The steps to make the recipe')

        # Sending the form.
        # Expect to successfully save the recipe and redirect to
        # authors:dashboard
        form.submit()
        # Wait a while to page load
        self.sleep(1)

        # Finding the message container by the class
        # If the form was successfully saved, a success message
        # should be displayed
        message_div = self.browser.find_element(
            By.CLASS_NAME, 'message-success')

        # Assertions:
        # Check if the success message was found in the message_div.text
        self.assertIn(
            'Your recipe was saved successfully!',
            message_div.text,
            msg='DASHBOARD_NEW_RECIPE - SAVING NEW RECIPE: The success '
            'message was not found.'
        )

        # Finding the div which holds the recipes as <li>
        recipes_list = self.browser.find_element(
            By.CLASS_NAME, 'authors-dashboard-list')

        # Finding all li elements inside the above list
        recipes = recipes_list.find_elements(
            By.CLASS_NAME, 'authors-dashboard-list-item')

        # Assertions:
        # Check if the recipes variable holds only one elemente
        # (the one recipe created by submiting the form)
        self.assertEqual(
            len(recipes),
            1,
            msg='DASHBOARD_NEW_RECIPE - NUMBER OF RECIPES: The list of recipes '
            'did not have the expect quantity. '
            f'Found: {len(recipes)}'
        )

        # Clicking in the first anchor in 'recipes' list
        recipes[0].find_element(By.TAG_NAME, 'a').click()

        # Wait a while to page load
        self.sleep(1)

        # Getting the form with recipe's information
        # Expect to display saved recipe data
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the input and textarea inputs
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Assertions:
        # Check if each field display the respective data

        # Title
        self.assertIn(
            'MyRecipeTitle',
            title_input.get_attribute('value'),
            msg='DASHBOARD_NEW_RECIPE - RECIPE TITLE: Expected title '
            'input value not found.'
        )

        # Description
        self.assertIn(
            'The recipe description',
            description_input.get_attribute('value'),
            msg='DASHBOARD_NEW_RECIPE - RECIPE DESCRIPTION: Expected  '
            'description input value not found.'
        )

        # Preparation time
        self.assertIn(
            '12',
            preparation_time_input.get_attribute('value'),
            msg='DASHBOARD_NEW_RECIPE - RECIPE PREPARATION TIME: Expected  '
            'preparation time input value not found.'
        )

        # Servings
        self.assertIn(
            '2',
            servings_input.get_attribute('value'),
            msg='DASHBOARD_NEW_RECIPE - RECIPE SERVINGS: Expected  '
            'servings input value not found.'
        )

        # Preparation steps
        self.assertIn(
            'The steps to make the recipe',
            text_area_field.text,
            msg='DASHBOARD_NEW_RECIPE - RECIPE PREPARATION STEPS: Expected  '
            'preparation steps input value not found.'
        )

    # TEST if invalid form is not accept and if error
    # message is displayed to the user
    def test_dashboard_new_recipe_invalid_form(self):

        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()

        # Wait a while to page load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the input and textarea fields
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Using send_keys to insert desired texts
        # The title value is invalid (less than 6 chars)
        title_input.send_keys('Small')
        description_input.send_keys('MyDescription')
        preparation_time_input.send_keys('2')
        servings_input.send_keys('3')
        text_area_field.send_keys('The steps to make the recipe')

        # Submiting the form
        form.submit()

        # Wait a while to page load
        self.sleep(1)

        # Getting the body of the new page
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Assertions:
        # Check if the error message was found in the page
        # Error message:
        #       'There are errors in the form, please fix them
        #        and try again.'
        # The error message should be displayed to the user

        self.assertIn(
            'There are errors in the form, please fix them and try again.',
            body,
            msg='DASHBOARD_NEW_RECIPE - INVALID FORM: Expected  '
            'error not found. Expected: There are errors in the form, '
            'please fix them and try again. Erro inserted: Title too small'
        )

    # TEST the dashboard_new_recipe with invalid prep_time
    # raises error
    def test_dashboard_new_recipe_with_invalid_prep_time(self):
        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()

        # Wait a while to load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the input and textarea inputs
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Inserting valid values, except to preparation time input field
        # Preparation time should be a positive number
        title_input.send_keys('A Valid Title')
        description_input.send_keys('A valid description')
        preparation_time_input.send_keys('-2')
        servings_input.send_keys('3')
        text_area_field.send_keys('The steps to make the recipe')

        # Submiting the form
        form.submit()

        # Wait a while to page load
        self.sleep(1)

        # Getting the new page body
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Assertions:
        # Check if the error message is displayed to the user
        # Error message expected:
        #       'Must be a positive number.'
        self.assertIn(
            'Must be a positive number.',
            body,
            msg='DASHBOARD_NEW_RECIPE - INVALID FORM: Expected  '
            'error not found. Expected: Required '
        )

    # TEST if invalid servings value raises error
    def test_dashboard_new_recipe_with_invalid_servings(self):
        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()

        # Wait a while to load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the input and textarea inputs
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Inserting valid values, except to servings input field
        # Servings should be a positive number
        title_input.send_keys('A Valid Title')
        description_input.send_keys('A valid description')
        preparation_time_input.send_keys('2')
        servings_input.send_keys('-3')
        text_area_field.send_keys('The steps to make the recipe')

        # Submiting the form
        form.submit()

        # Wait a while to page load
        self.sleep(1)

        # Getting the new page body
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Assertions:
        # Check if the error message is displayed to the user
        # Error message expected:
        #       'Must be a positive number.'
        self.assertIn(
            'Must be a positive number.',
            body,
            msg='DASHBOARD_NEW_RECIPE - INVALID FORM: Expected  '
            'error not found. Expected: Required '
        )

    # TEST if equals description and title raises error
    def test_dashboard_new_recipe_title_descr_equals(self):
        # my_user login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # Finding the anchor element to a new recipe by its class
        new_recipe = self.browser.find_element(
            By.CLASS_NAME, 'dashboard-new-recipe')

        # Clicking in it
        new_recipe.click()

        # Wait a while to page load
        self.sleep(1)

        # Getting the form with recipe's information
        # It is expected to be blank.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Getting the input and textarea fields
        title_input = form.find_element(By.ID, 'id_title')
        description_input = form.find_element(By.ID, 'id_description')
        preparation_time_input = form.find_element(
            By.ID, 'id_preparation_time')
        servings_input = form.find_element(By.ID, 'id_servings')
        text_area_field = form.find_element(By.TAG_NAME, 'textarea')

        # Inserting valid values. BUT title and description equals
        # It should invalidate the form, raising an error to the user
        title_input.send_keys('A generic text')
        description_input.send_keys('A generic text')
        preparation_time_input.send_keys('2')
        servings_input.send_keys('-3')
        text_area_field.send_keys('The steps to make the recipe')

        # Submiting the form
        form.submit()
        # Wait a while to page load
        self.sleep(1)

        # Getting the new page body
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Assertions:
        # Check if the error message is displayed to the user
        # Error message expected:
        #       'Must be different from title'
        self.assertIn(
            'Must be different from title',
            body,
            msg='DASHBOARD_NEW_RECIPE - INVALID FORM: Expected  '
            'error not found. Expected: Must be different from title '
        )

        # Check if the error message is displayed to the user
        # Error message expected:
        #       'Must be different from description'
        self.assertIn(
            'Must be different from description',
            body,
            msg='DASHBOARD_NEW_RECIPE - INVALID FORM: Expected  '
            'error not found. Expected: Must be different from description '
        )
