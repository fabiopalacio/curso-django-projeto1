from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from tag.models import Tag
from tag.serializers import TagSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':

        recipes = Recipe.objects.get_published()[:7]
        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        
        return Response('POST', status=status.HTTP_201_CREATED)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)

    serializer = RecipeSerializer(
        recipe, many=False, context={'request': request})
    return Response(serializer.data)


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(
        tag, many=False, context={'request': request})
    return Response(serializer.data)
