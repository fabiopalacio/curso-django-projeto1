from django.urls import path  # type: ignore
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
