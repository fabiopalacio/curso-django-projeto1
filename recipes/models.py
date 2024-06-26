from collections import defaultdict
from django.contrib.auth.models import User  # type: ignore
from django.db import models
from django.forms import ValidationError
from django.urls import reverse  # type: ignore
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)

    slug = models.SlugField(unique=True)

    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(
        max_length=65)

    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)

    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(
        default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)

    cover = models.ImageField(
        upload_to='recipes/cover/%Y/%m/%d/', blank=True, default='')

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None)

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipes_from_db = Recipe.objects.filter(
            title__iexact=self.title
        )

        for recipe in recipes_from_db:
            if recipe.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with this title.'
                    'Please choose another one.')
                break

        if error_messages:
            raise ValidationError(error_messages)
