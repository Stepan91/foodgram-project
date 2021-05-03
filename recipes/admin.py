from django.contrib import admin
from .models import Recipe, Ingredient, IngredientRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'tag', 'pub_date')
    search_fields = ('author', 'title')
    list_filter = ('author', 'title', 'tag')
    inlines = (IngredientRecipeInline,)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
