from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator
from .models import Recipe, Ingredient, User


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )
