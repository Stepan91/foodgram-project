from django import template
from recipes.models import Favorite, Purchase
register = template.Library()


@register.filter
def fav_exists(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def purch_exists(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()
