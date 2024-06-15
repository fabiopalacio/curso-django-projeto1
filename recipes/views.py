import os
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.http import Http404

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
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
    # template_name -> required because django uses
    # f'{context_object_name}_list.html'
    # If this is not the template's name, change here
    template_name = 'recipes/pages/home.html'


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
