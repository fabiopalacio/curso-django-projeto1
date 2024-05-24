from django.urls import path  # type: ignore
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),

    path('login/', views.login_view, name='login'),
    path('login/auth/', views.login_auth, name='login_auth'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path(
        'dashboard/recipe/new',
        views.recipe_new,
        name='dashboard_recipe_new'),

    path(
        'dashboard/recipe/create',
        views.create_recipe,
        name='dashboard_recipe_create'),

    path(
        'dashboard/recipe/<int:id>/edit',
        views.dashboard_recipe,
        name='dashboard_recipe'),


]
