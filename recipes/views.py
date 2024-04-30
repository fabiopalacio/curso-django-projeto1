from django.shortcuts import render
from django.http import HttpResponse  # type: ignore
# Create your views here.


def my_view(request):
    return HttpResponse('Uma linda String')
