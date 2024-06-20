from django.forms import model_to_dict
from django.http import JsonResponse
import os
from django.db.models import Q
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import DetailView, ListView
from django.http import Http404

from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def get_path_to_media(self):
    '''
        Method to recover the domain
    '''
    return self.request.build_absolute_uri(
    )[:self.request.build_absolute_uri().find('recipes')] + 'media/'


def set_path_to_media(self, recipe):
    '''
        Method to adjust the link to the recipes medias
    '''
    if recipe.get('cover'):
        path_to_media = get_path_to_media(self)
        recipe['cover'] = path_to_media + recipe['cover'].name
    else:
        recipe['cover'] = ''
    return recipe


def set_author_name(recipe):
    '''
        Method to check author name
        The future API methods to interact with the application
        will be done by the author's id and category's id
        But the author's name and category's name should be available
        in the API.
        The author name is setted here to make it easy future
        adjustments in this logic.
    '''
    author_id = recipe.author.id

    author_name = recipe.author.first_name + \
        ' ' + recipe.author.last_name

    return author_id, author_name.strip()


def get_recipes(self, is_detailed=False):
    '''
        Method to recover the recipes to each view and return it
        prepared to be used in JsonResponse()
        Two situations here: first to detailed view (which search for 'recipe' context);
        and second to the remain views (which search for 'recipes' context)
    '''
    if is_detailed:
        recipe = self.get_context_data()['recipe']

        recipe_dict = model_to_dict(recipe)

        author_id, author_name = set_author_name(recipe)

        recipe_dict['author_id'] = author_id
        recipe_dict['author_name'] = author_name

        recipe_dict = set_path_to_media(self, recipe_dict)

        recipe_dict['category_id'] = recipe_dict['category']
        recipe_dict['category_name'] = recipe.category.name

        del recipe_dict['author']
        del recipe_dict['category']

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['update_at'] = str(recipe.update_at)

        return recipe_dict

    else:
        recipes = self.get_context_data()['recipes']
        recipes_list = list()

        for recipe in recipes:
            category_name = recipe.category.name
            author_id, author_name = set_author_name(recipe)

            recipe = model_to_dict(recipe)

            recipe['author_id'] = author_id
            recipe['author_name'] = author_name

            recipe['category_id'] = recipe['category']
            recipe['category_name'] = category_name

            del recipe['author']
            del recipe['category']

            recipe = set_path_to_media(self, recipe)

            recipes_list.append(recipe)

        return recipes_list


class RecipeListViewBase(ListView):
    '''
        Base View to all recipes views
        Holds the default conf
    '''
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
        qs = qs.prefetch_related('tags')

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

        # Update the get_context_data with two new entries got above:
        #   recipes with the recipes to be displayed in the current page
        #   pagination_range with the pagination_range returned above
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range
        })

        # Return the new context
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    '''
        template_name -> required because django uses
        f'{context_object_name}_list.html'
        If this is not the template's name, change here
    '''
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeAPI(RecipeListViewHome):

    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self, is_detailed=False)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=True,
            category_id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f"{ctx.get('recipes')[0].category.name} - Category |"
        })

        return ctx


class RecipeListViewCategoryAPI(RecipeListViewCategory):
    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) | Q(
                    description__icontains=search_term)),
            is_published=True,)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        ctx.update({
            'page_title': f'Looking for "{ search_term }"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })

        return ctx


class RecipeListViewSearchAPI(RecipeListViewSearch):
    def render_to_response(self, context, **response_kwargs):

        recipes = get_recipes(self)

        return JsonResponse(
            recipes,
            safe=False
        )


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            id=self.kwargs.get('pk'),
            is_published=True
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'isDetailPage': True
        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = get_recipes(self, is_detailed=True)

        return JsonResponse(
            recipe,
            safe=False
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'Tag "{page_title}" '

        ctx.update({
            'page_title': page_title,

        })

        return ctx
