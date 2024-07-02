from django.forms import model_to_dict
from django.http import JsonResponse
import os
from django.db.models import Q
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.utils import translation
from django.utils.translation import gettext as _

from recipes.models import Recipe
from tag.models import Tag
from utils.i18n import set_language
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def get_path_to_media(self):
    # Method to recover the url to media folder.
    # self.request.build_absolute_uri() returns the full uri, but here
    # it is required only the domain. The first thing after the domain
    # is 'recipes. So the str is cutted where recipes is found
    # and is concated with 'media/', which is the folder where the medias
    # are saved. This method allows the set_path_to_media() to create the
    # correct link to the media

    return self.request.build_absolute_uri(
    )[:self.request.build_absolute_uri().find('recipes')] + 'media/'


def set_path_to_media(self, recipe):
    # Method to adjust the link to the recipes medias
    # It get the path to media folder from get_path_to_media()
    # and add the cover name from recipe.
    # If no cover was passed to recipe, it uses an empty string
    # and them return the recipe adjusted.
    if recipe.get('cover'):
        path_to_media = get_path_to_media(self)
        recipe['cover'] = path_to_media + recipe['cover'].name
    else:
        recipe['cover'] = ''
    return recipe


def set_author_name(recipe):
    # Method to check author name
    #     The future API methods to interact with the application
    #     will be done by the author's id and category's id
    #     But the author's name and category's name should be available
    #     in the API.

    author_id = recipe.author.id

    author_name = recipe.author.first_name + \
        ' ' + recipe.author.last_name

    return author_id, author_name.strip()


def adjust_recipe(self, recipe):
    # Method to adjust the recipe to be passed as JSON
    # It converts the recipe model to dict and adjust
    # some values
    #
    # Any interaction with the application should be done
    # by IDs. So here is created new keys to recipe dict,
    # allowing API to know the authors and category's names,
    # but also knowing their IDs, if necessary.
    #
    # This variables are created to be easier to use their
    # values. It was easier to work with recipe model here,
    # so the values are saved before recipe convertion
    # to dict
    category_name = recipe.category.name
    author_id, author_name = set_author_name(recipe)
    created_at = recipe.created_at

    # Here recipe become a dict
    recipe = model_to_dict(recipe)

    # Creating new keys to recipe dict.
    # Author's name to be display to users
    # Author's id to interact with application
    recipe['author_name'] = author_name
    recipe['author_id'] = author_id

    # Creating new keys to recipe dict.
    # Category's name to be display to users
    # Category's id to interact with application
    # recipe['category'] returns the id
    # (after the model_to_dict() method)
    recipe['category_name'] = category_name
    recipe['category_id'] = recipe['category']

    # Adjusting the link to recipe's cover
    recipe = set_path_to_media(self, recipe)

    # Adjusting the tags to be passed as JSON
    # The decision here was to use a string with
    # each tag separated by comma.
    tag_list = ''
    for tag in recipe['tags']:
        tag_list += tag.name + ', '

    # Removing the last char because it will add a comma
    # after the last tag
    tag_list = tag_list.strip()[:-1]

    # Removing the key-values that were adjusted here to be
    # passed as JSON. Their values are saved in different keys above
    del recipe['tags']
    del recipe['author']
    del recipe['category']

    # Creating new keys
    recipe['tags'] = tag_list
    recipe['created_at'] = str(created_at)

    return recipe


def get_recipes(self, is_detailed=False):
    # Method to recover the recipes to each view and return it
    # prepared to be used in JsonResponse()
    # Two situations here: first to detailed view (which search for
    # 'recipe' context); and second to the remain views (which
    # search for 'recipes' context)
    if is_detailed:

        recipe = self.get_context_data()['recipe']
        return adjust_recipe(self, recipe)

    else:
        recipes = self.get_context_data()['recipes']
        recipes_list = list()

        for recipe in recipes:
            recipe = adjust_recipe(self, recipe)
            recipes_list.append(recipe)

        return recipes_list


class RecipeListViewBase(ListView):

    # Base View to all recipes views
    # Holds the default conf

    model = Recipe
    context_object_name = 'recipes'

    # paginate_by = None because I am using the utils/pagination.py
    # that was created in the course
    paginate_by = None

    # Order the data by descending ids
    ordering = ['-id']

    # get_querysey -> to manipulate the queryset
    # Here it is required to filter the unpublished recipes

    def get_queryset(self, *args, **kwargs):

        # Getting the queryset super()
        qs = super().get_queryset(*args, **kwargs)

        # Overwriting it with the filtered one
        qs = qs.filter(
            is_published=True
        )

        # Performance boost; returns a queryset that will follow
        # foreign key relationships selecting additional related-object
        # data when it executes its query.
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')

        # Returning the new super().get_queryset
        return qs

    # get_context_data -> to manipulate the context data
    # Required here to use our pagination system

    def get_context_data(self, *args,  **kwargs):

        # Get the super().get_context_data
        ctx = super().get_context_data(*args, **kwargs)

        # get the make_pagination() return:
        # page_obj -> recipes to be displayed in the current page
        # pagination_range -> multiple values:
        # pagination : the first and last page to be displayed in the
        #       navigation
        # page_range: pages'list
        # qty_pages: number of pages to be displayed in the navigation
        # current_page: The current page
        # total_pages: number of pages = len(page_range)
        # start_range: first page to be displayed in navigation
        # stop_range: last page to be displayed in navigation
        # first_page_out_of_range: Is the first page out of range in
        #       navigation? (boolean)
        # last_page_out_of_range: Is the last page out of range in
        #       navigation? (boolean)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE)

        # Getting the browser language
        html_language = translation.get_language()

        # Update the get_context_data with two new entries got above:
        #   recipes with the recipes to be displayed in the current page
        #   pagination_range with the pagination_range returned above
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'html_language': html_language,
        })

        # Return the new context
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    # template_name -> required because django uses
    #     f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeAPI(RecipeListViewHome):
    # View to be used as API, returning JSON with home data
    def render_to_response(self, context, **response_kwargs):
        # Overwriting render_to_response() to return the JSON
        # with requested data.
        # This logic was moved to method get_recipes()
        # to avoid repetition
        # and to let the view code cleaner.
        # The parameter is_detailed=False allow the method
        # to search to the specific context.
        # Detail view uses recipe (singular)
        # and the remaining views use recipes (plural)
        recipes = get_recipes(self, is_detailed=False)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    # template_name -> required because django uses
    #     f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        # Overwriting the get_queryset method
        # It calls the RecipeListViewBase get_queryset
        # and does a new filter, getting only the
        # recipes with the desired category
        # (filtered by category_id)
        # Here the is_published is added to the filter
        # only as a guarantee (It is used in super().get_queryset)
        # Empty queryset is treated as error and raises 404
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=True,
            category_id=self.kwargs.get('category_id')
        )
        # If the returned queryset is empty, raises 404
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        # Overwriting get_context_data to create page title
        # based on the category required
        # It updates the context data, adding a new
        # entry called title, which will be used in the template
        # to change the page title
        ctx = super().get_context_data(*args, **kwargs)

        category_translation = _('Category')
        ctx.update({
            'title': f"{ctx.get('recipes')[0].category.name} - "
            f"{category_translation} |"
        })

        return ctx


class RecipeListViewCategoryAPI(RecipeListViewCategory):
    # Overwriting render_to_response() to return the JSON with requested data.
    # This logic was moved to method get_recipes() to avoid repetition
    # and to let the view code cleaner.
    # The parameter is_detailed=False allow the method to search to the specific
    # context. Detail view uses recipe (singular) and the remaining views use
    # recipes (plural)
    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeListViewSearch(RecipeListViewBase):
    # template_name -> required because django uses
    #     f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        # Overwriting the get_queryset method
        # It calls the RecipeListViewBase get_queryset
        # and does a new filter, getting only the
        # recipes with the desired category
        # (filtered by category_id)
        # Here the is_published is added to the filter
        # only as a guarantee (It is used in super().get_queryset)
        # Empty queryset is treated as error and raises 404
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) | Q(
                    description__icontains=search_term)),
            is_published=True,)

        return qs

    def get_context_data(self, *args, **kwargs):
        # Overwriting get_context_data to create page title
        # based on the search term typed
        # It updates the context data, adding a new
        # entry called title, which will be used in the template
        # to change the page title
        # It also pass the search term and additional url query
        # If no search term is passed, raises a 404 error
        ctx = super().get_context_data(*args, **kwargs)

        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()
        prev_page_title = _('Looking for ')
        ctx.update({
            'page_title': f'{prev_page_title} "{ search_term }"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })

        return ctx


class RecipeListViewSearchAPI(RecipeListViewSearch):
    # Overwriting render_to_response() to return the JSON with requested data.
    # This logic was moved to method get_recipes() to avoid repetition
    # and to let the view code cleaner.
    # The parameter is_detailed=False allow the method to search to the specific
    # context. Detail view uses recipe (singular) and the remaining views use
    # recipes (plural)
    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeDetail(DetailView):
    # Define the model (require to DetailView)
    model = Recipe

    # Define the context_object_name as recipe
    # which will be used to get the context data
    context_object_name = 'recipe'
    # template_name -> required because django uses
    #     f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        # get_querysey -> to manipulate the queryset
        # Here it is required to filter the unpublished recipes out of
        # queryset (showing only the published ones)
        # and uses the pk to filter the recipes, keeping
        # only the desired one
        # If no recipe is found with that pk,
        # raises 404
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            id=self.kwargs.get('pk'),
            is_published=True
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        # Get the context data from parent (method super)
        # and update the context, adding the isDetailPage to be True
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'isDetailPage': True,
            'html_language': set_language(),

        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    # Overwriting render_to_response() to return the JSON with requested data.
    # This logic was moved to method get_recipes() to avoid repetition
    # and to let the view code cleaner.
    # The parameter is_detailed=True allow the method to search to the specific
    # context. Detail view uses recipe (singular) and the remaining views use
    # recipes (plural)
    def render_to_response(self, context, **response_kwargs):
        recipe = get_recipes(self, is_detailed=True)

        return JsonResponse(
            recipe,
            safe=False
        )


class RecipeListViewTag(RecipeListViewBase):
    # template_name -> required because django uses
    #     f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        # get_querysey -> to manipulate the queryset
        # Filter the recipes that have the same tag as passed
        # by url
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(tags__name=self.kwargs.get('tag_name', ''))

        return qs

    def get_context_data(self, *args, **kwargs):
        # Overwriting get_context_data to create page title
        # based on the tag name required

        ctx = super().get_context_data(*args, **kwargs)

        tag = Tag.objects.filter(
            name=self.kwargs.get('tag_name', '')).first()

        if not tag:
            page_title = 'No recipes found'
        else:
            page_title = f'Tag "{tag.name}" '

        ctx.update({
            'page_title': page_title,

        })

        return ctx


class RecipeListViewTagAPI(RecipeListViewTag):

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if not qs:
            raise Http404()
        else:
            return qs
    # Overwriting render_to_response() to return the JSON with requested data.
    # This logic was moved to method get_recipes() to avoid repetition
    # and to let the view code cleaner.

    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self)

        return JsonResponse(
            recipes,
            safe=False
        )
