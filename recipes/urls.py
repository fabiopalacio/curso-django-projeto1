"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path  # type: ignore

from .views import site, api

app_name = 'recipes'

urlpatterns = [
    path('', site.RecipeListViewHome.as_view(), name='home'),

    path(
        'recipes/search/',
        site.RecipeListViewSearch.as_view(),
        name='search'),

    path(
        'recipes/category/<int:category_id>/',
        site.RecipeListViewCategory.as_view(),
        name='category'),

    path(
        'recipes/<int:pk>/',
        site.RecipeDetail.as_view(),
        name='recipe'),

    path(
        'recipes/tag/<str:tag_name>/',
        site.RecipeListViewTag.as_view(),
        name='tag'),

    # API
    path(
        'recipes/api/v1/',
        site.RecipeListViewHomeAPI.as_view(),
        name='recipes_api_v1'),

    path(
        'recipes/api/v1/<int:pk>/',
        site.RecipeDetailAPI.as_view(),
        name='recipe_api_v1'),

    path(
        'recipes/api/v1/category/<int:category_id>/',
        site.RecipeListViewCategoryAPI.as_view(),
        name='category_api_v1'),

    path(
        'recipes/api/v1/search/',
        site.RecipeListViewSearchAPI.as_view(),
        name='search_api_v1'),


    path(
        'recipes/api/v1/tag/<str:tag_name>/',
        site.RecipeListViewTagAPI.as_view(),
        name='tag_api_v1'),

    # DJANGO REST FRAMEWORK
    path(
        'recipes/api/v2/',
        api.recipe_api_list,
        name='recipes_api_v2'),



]
