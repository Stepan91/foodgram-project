from django import template
from recipes.models import Recipe
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def counter(recipes, author):
    cnt = Recipe.objects.filter(author=author).count()
    if cnt < 3:
        return
    else:
        cnt -= 3
        if cnt in range(2, 5) or cnt % 10 in range(2, 5):
            return f'{cnt} рецепта'
        elif cnt in range(5, 21) or cnt % 10 in range(5, 10) or cnt % 10 == 0:
            return f'{cnt} рецептов'
        elif cnt % 10 == 1:
            return f'{cnt} рецепт'
