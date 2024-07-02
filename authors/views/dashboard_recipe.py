from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.contrib import messages  # type: ignore
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from authors.forms.recipe_form import AuthorsRecipeForm
from recipes.models import Recipe

from utils.i18n import set_language


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'),
    name='dispatch')
class DashboardRecipe(View):

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id=id).first()
            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            self.request, 'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
                'btn_text': 'Send...',
                'html_language': set_language()
            })

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorsRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):

        recipe = self.get_recipe(id)

        form = AuthorsRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Your recipe was saved successfully!')
            return redirect(reverse('authors:dashboard'))

        return self.render_recipe(form)


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'),
    name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, request, *args, **kwargs):
        recipe = self.get_recipe(id=request.POST.get('id'))
        recipe.delete()
        messages.success(request, 'Your recipe was deleted.')
        return redirect(reverse('authors:dashboard'))


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'),
    name='dispatch')
class DashboardList(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    template_name = 'authors/pages/dashboard_view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=False,
            author=self.request.user
        )

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'html_language': set_language(),
        })
        return ctx
