from django import template
from api.models import Favorite, Purchase, Follow
from recipes.models import IngredientRecipe

register = template.Library()


@register.filter
def ingredient_for_recipe(ingredientrecipes, recipe):
    return IngredientRecipe.objects.filter(recipe=recipe)


@register.filter
def favorite_exists(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def purchase_exists(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def follow_exists(author, user):
    return Follow.objects.filter(author=author, user=user).exists()


@register.simple_tag
def set_tags(request, value):
    request_object = request.GET.copy()
    tags = request_object.getlist('tag')
    if value in tags:
        tags.remove(value)
        request_object.setlist('tag', tags)
    else:
        tags.append(value)
        request_object.setlist('tag', tags)
    return request_object.urlencode()
