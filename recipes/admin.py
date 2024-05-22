from django.contrib import admin
from .models import Category, Recipe
# Register your models here.
# Two ways to register a model. Using the admin.site.register
# (ClassImported, ClassAdminCreatedHere) and
# using the @admin.register(ClassImported)
# before the creation of the ClassAdmin.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'created_at',
        'is_published', 'category', 'author')
    list_display_links = ('title', 'created_at')
    list_editable = ('is_published',)

    search_fields = ('title', 'description', 'author__first_name', )

    list_filter = (
        'category', 'author', 'is_published',
        'preparation_steps_is_html')

    list_per_page = 10
    ordering = ('-id',)
    prepopulated_fields = {
        'slug': ('title', )
    }


admin.site.register(Category, CategoryAdmin)
