from django.contrib import admin
from .models import (
    Recipe, Ingredient, IngredientRecipe,
    Follow, Favorite, Purchase
)


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


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
