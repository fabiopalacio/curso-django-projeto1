from collections import defaultdict

from django.contrib.auth.models import User  # type: ignore
from django.db import models
from django.urls import reverse  # type: ignore
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tag.models import Tag
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Recipe(models.Model):
    title = models.CharField(
        max_length=65, unique=True, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description'))

    slug = models.SlugField(unique=True)

    preparation_time = models.IntegerField(verbose_name=_('Preparation Time'))

    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_('Preparation time unit'))

    servings = models.IntegerField(verbose_name=_('Servings'))

    servings_unit = models.CharField(
        max_length=65, verbose_name=_('Servings unit'))

    preparation_steps = models.TextField(verbose_name=_('Preparation Steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'))
    update_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at'))

    is_published = models.BooleanField(
        default=False, verbose_name=_('Is it published?'))

    cover = models.ImageField(
        upload_to='recipes/cover/%Y/%m/%d/', blank=True, default='',
        verbose_name=_('Cover Image'))

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None, verbose_name=_('Category'))

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('Author'))

    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name=_('Tags'))

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
