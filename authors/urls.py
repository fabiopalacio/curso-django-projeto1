from django.urls import path  # type: ignore
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),

    path('login/', views.login_view, name='login'),
    path('login/auth/', views.login_auth, name='login_auth'),
    path('logout/', views.logout_view, name='logout'),

]
