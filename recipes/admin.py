from django.contrib import admin
from .models import Category, Recipe
# Register your models here.
# Two ways to register a model. Using the admin.site.register(ClassImported, ClassAdminCreatedHere) and
# using the @admin.register(ClassImported) before the creation of the ClassAdmin.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
