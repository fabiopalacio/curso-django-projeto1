from rest_framework import serializers

from recipes.models import Category, Recipe, Tag

from django.contrib.auth.models import User

from tag.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'preparation', 'category_name',
            'category', 'author_name', 'author', 'public', 'tags',
            'tags_objects', 'tags_links']

    public = serializers.BooleanField(source='is_published', read_only=True,)

    preparation = serializers.SerializerMethodField(
        method_name='get_preparation', read_only=True,)

    category_name = serializers.StringRelatedField(source='category')

    author_name = serializers.StringRelatedField(source='author')

    tags_objects = TagSerializer(
        many=True,
        source='tags', read_only=True,
    )

    tags_links = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='recipes:tag_detail_api_v2',
        source='tags', read_only=True,

    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
