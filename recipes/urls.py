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
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),

    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name='search'),

    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name='category'),

    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name='recipe'),

    path(
        'recipes/tag/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name='tag'),

    # API
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeAPI.as_view(),
        name='recipes_api_v1'),

    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name='recipe_api_v1/'),

    path(
        'recipes/api/v1/category/<int:category_id>/',
        views.RecipeListViewCategoryAPI.as_view(),
        name='recipes_category_api_v1/'),

    path(
        'recipes/api/v1/search/',
        views.RecipeListViewSearchAPI.as_view(),
        name='recipes_search_api_v1/'),
]
