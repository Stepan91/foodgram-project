from django import template
from api.models import Favorite, Purchase, Follow
from recipes.models import IngredientRecipe

register = template.Library()


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


@register.filter
def counter(recipes, author):
    cnt = author.recipes.count()
    if cnt <= 3:
        return
    cnt -= 3
    if cnt in range(2, 5) or cnt % 10 in range(2, 5):
        return f'{cnt} рецепта'
    elif cnt in range(5, 21) or cnt % 10 in range(5, 10) or cnt % 10 == 0:
        return f'{cnt} рецептов'
    elif cnt % 10 == 1:
        return f'{cnt} рецепт'
