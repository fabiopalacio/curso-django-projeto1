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

    public = serializers.BooleanField(source='is_published')

    preparation = serializers.SerializerMethodField(
        method_name='get_preparation')

    category_name = serializers.StringRelatedField(source='category')

    author_name = serializers.StringRelatedField(source='author')

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    tags_objects = TagSerializer(
        many=True,
        source='tags'
    )

    tags_links = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        view_name='recipes:tag_detail_api_v2',
        source='tags'

    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
