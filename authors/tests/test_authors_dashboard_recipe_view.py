from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, Category


class DashboardTest(TestCase):
    def create_user_and_recipe(self):
        password = 'my_password'
        username = 'my_user'
        my_user = User.objects.create_user(
            username=username, password=password)
        self.client.login(
            username=username, password=password)

        category = Category.objects.create(name='My_category')

        recipe = Recipe.objects.create(
            category=category,
            author=my_user,
            title='My title',
            description='description',
            slug='my-title',
            preparation_time=1,
            preparation_time_unit='Horas',
            servings=2,
            servings_unit='Pessoas',
            preparation_steps='preparation_steps',
            preparation_steps_is_html=False,
            is_published=False,)

        return recipe, my_user, category

    def setUp(self, *args, **kwargs):
        self.recipe, self.my_user, self.category = self.create_user_and_recipe()
        return super().setUp(*args, **kwargs)

    def test_dashboard_list_view_get_method(self):

        url = reverse('authors:dashboard')
        response = self.client.get(url, follow=True)

        self.assertEqual(
            response.status_code,
            200,
            msg="DASHBOARD_RECIPE - STATUS-CODE: Get page returned wrong "
            "status code. Expected: 200. "
            f"Found: {response.status_code}"
        )

        self.assertIn(
            '<title>  Dashboard my_user |  Recipes</title>',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE - PAGE TITLE: Page title not found "
            "in html."
        )

        self.assertIn(
            'My title',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE - RECIPE TITLE: Recipe title not found "
            "in html."
        )

        self.assertContains(
            response,
            '<i class="fa-solid fa-xmark"></i>',
            1,
            msg_prefix='DASHBOARD_RECIPE - RECIPE DELETE OPTION: There are '
            'wrong number of delete recipes buttons'
        )

    def test_dashboard_recipe_view_get_method_with_id(self):
        url = reverse('authors:dashboard_recipe', kwargs={'id': 1})
        response = self.client.get(url, follow=True)

        self.assertIn(
            'My title',
            response.content.decode('utf-8'),
            msg='DASHBOARD_RECIPE - RECIPE TITLE: Recipe title was not found '
            'in the html. Title: My title'
        )

        self.assertEqual(
            response.status_code,
            200,
            msg='DASHBOARD_RECIPE - STATUS CODE: The status code returned was '
            f'not expected. Found: {response.status_code}'
        )

        self.assertContains(
            response,
            status_code=200,
            text='<input',
            count=6)

    def test_dashboard_recipe_view_get_method_without_id(self):

        url = reverse('authors:dashboard_recipe_new')
        response = self.client.get(url, follow=True)

        self.assertContains(
            response,
            status_code=200,
            text='<input',
            count=6)

        # Description input has no value
        self.assertIn(
            '<input type="text" name="description" maxlength="165" required '
            'id="id_description">',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE_NEW - DESCRIPTION FIELD: Description field "
            "was not empty."
        )

        # Title input has no value
        self.assertIn(
            '<input type="text" name="title" maxlength="65" '
            'required id="id_title">',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE_NEW - TITLE FIELD: Title field "
            "was not empty."
        )

        # PREPARATION TIME input has no value
        self.assertIn(
            '<input type="number" name="preparation_time" '
            'required id="id_preparation_time">',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE_NEW - PREPARATION TIME FIELD: Preparation "
            "time field was not empty."
        )

        # SERVINGS input has no value
        self.assertIn(
            '<input type="number" name="servings" required id="id_servings">',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE_NEW - SERVINGS FIELD: Servings "
            "field was not empty."
        )

        # PREPARATION_STEPS textarea has no value
        self.assertIn(
            '<textarea name="preparation_steps" cols="40" rows="10" '
            'class="span-2" required id="id_preparation_steps">\n</textarea>',
            response.content.decode('utf-8'),
            msg="DASHBOARD_RECIPE_NEW - SERVINGS FIELD: Preparation steps "
            "field was not empty."
        )

    def test_dashboard_recipe_view_get_404_no_recipe_found(self):
        url = reverse('authors:dashboard_recipe', kwargs={'id': 123})
        response = self.client.get(url, follow=True)

        self.assertEqual(
            404,
            response.status_code,
            msg='DASHBOARD_RECIPE - NO RECIPE STATUS CODE: The status code '
            'returned was incorrect. Expected: 404. '
            f'Found: {response.status_code}'
        )

    #
    # O ERRO ESTÁ AQUI
    # CORRIGIR
    # COMO FAZER POST?
    def test_dashboard_recipe_view_post_method(self):

        # making the recipe to be invalid

        form_data = {
            'category': self.category,
            'author': self.my_user,
            'title': 'small',
            'description': 'description',
            'slug': 'my-title',
            'preparation_time': 1,
            'preparation_time_unit': 'Horas',
            'servings': 2,
            'servings_unit': 'Pessoas',
            'preparation_steps': 'preparation_steps',
            'preparation_steps_is_html': False,
            'is_published': False,
        }

        url = reverse(
            'authors:dashboard_recipe',
            kwargs={'id': self.recipe.id})

        response = self.client.post(url, form_data, follow=True)

        self.assertIn(
            'Must have at least 6 characters.',
            response.content.decode('utf-8'),
            msg='DASHBOARD_RECIPE - POST METHOD: Title error not found in'
            ' the html response.'
        )

        self.assertIn(
            'Must have at least 6 characters.',
            response.context['form'].errors.get('title'),
            msg='DASHBOARD_RECIPE - POST METHOD: Title error not found in'
            ' the html response.'
        )

        form_data['title'] = 'Large enough'
        response = self.client.post(url, form_data)

        self.assertNotIn(
            'Must have at least 6 characters.',
            response.content.decode('utf-8'),
            msg='DASHBOARD_RECIPE - POST METHOD: Title error not found in'
            ' the html response.'
        )

    def test_dashboard_delete_view_remove_recipe(self):
        recipe = Recipe.objects.create(
            category=self.category,
            author=self.my_user,
            title='MyNewRecipe',
            description='description 2',
            slug='my-title2',
            preparation_time=2,
            preparation_time_unit='Horas',
            servings=4,
            servings_unit='Pessoas',
            preparation_steps='preparation_steps',
            preparation_steps_is_html=False,
            is_published=False,)

        data = {
            'id': self.recipe.id
        }

        url_dashboard_list = reverse('authors:dashboard')
        response = self.client.get(url_dashboard_list)

        self.assertContains(
            response,
            '<i class="fa-solid fa-xmark">',
            2,
            200,
            msg_prefix='DASHBOARD_DELETE_RECIPE - NUMBER OF RECIPES: '
            'Wrong number of delete icons found.'
        )

        url_delete_recipe = reverse('authors:dashboard_delete_recipe')
        response = self.client.post(url_delete_recipe, data, follow=True)

        self.assertContains(
            response,
            '<i class="fa-solid fa-xmark">',
            1,
            200,
            msg_prefix='DASHBOARD_DELETE_RECIPE - NUMBER OF RECIPES: Wrong '
            'number of delete icons found.'
        )

        self.assertIn(
            recipe.title,
            response.content.decode('utf-8'),
            msg="DASHBOARD_DELETE_RECIPE - TITLE: The expected recipe was not "
            "found"
        )
