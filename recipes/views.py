from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import (
    Recipe, User, IngredientRecipe, Ingredient
)
from api.models import Follow, Favorite, Purchase
from .forms import RecipeForm
from .utils import save_recipe
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Q
from functools import reduce
import operator


def get_tags(request):
    tags = []
    tags_filter = None
    if request.GET.getlist('tag'):
        tags = request.GET.getlist('tag')
    if tags:
        tags_filter = reduce(
            operator.or_, (Q(tag__contains=tag) for tag in tags))
    tags = request.GET.getlist('tag')
    return tags, tags_filter


def index(request):
    tags, tags_filter = get_tags(request)
    if tags_filter:
        recipe_list = Recipe.objects.filter(tags_filter).all()
    else:
        recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        save_recipe(request, form)
        return redirect('index')
    return render(request, 'new.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    form = RecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        save_recipe(request, form)
        return redirect('index')
    return render(
        request,
        'recipe_edit.html',
        {'form': form, 'recipe': recipe}
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    form = RecipeForm()
    return render(
        request,
        'single_recipe.html',
        {'recipe': recipe, 'form': form}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    tags, tags_filter = get_tags(request)
    if tags_filter:
        recipe_list = Recipe.objects.filter(tags_filter).filter(author=author)
    else:
        recipe_list = Recipe.objects.filter(author=author)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = None
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author).exists()
    return render(
        request,
        'profile.html', {
            'page': page,
            'paginator': paginator,
            'author': author,
            'following': following,
            'tags': tags,
            }
        )


@login_required
def recipe_delete(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)
    if recipe.exists() and author == request.user:
        recipe.delete()
    return redirect('profile', username=username)


@login_required
def follow_index(request, username):
    authors = User.objects.filter(following__user__username=username)
    paginator = Paginator(authors, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator
        }
    )


@login_required
def favorites_view(request, username):
    tags, tags_filter = get_tags(request)
    if tags_filter:
        recipe_list = Recipe.objects.filter(tags_filter).filter(
            favorites__user__username=username
        )
    else:
        recipe_list = Recipe.objects.filter(favorites__user__username=username)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorites.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
    )


@login_required
def purchases_view(request, username):
    purchases = Purchase.objects.filter(user__username=username)
    recipe_list = Recipe.objects.filter(purchases__in=purchases)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'shoplist.html',
        {'page': page, 'paginator': paginator, 'purchases': purchases}
    )


def purchase_list(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)
    ingredients = Ingredient.objects.filter(
        ingredientrecipe__recipe__in=recipes
    )
    ingredient_recipes = IngredientRecipe.objects.filter(
        ingredient__in=ingredients,
        recipe__in=recipes
    )
    purchaselist = {}
    for item in ingredient_recipes:
        if purchaselist.get(item.ingredient.name) is None:
            purchaselist[item.ingredient.name] = [
                item.ingredient.unit,
                item.value
            ]
        else:
            purchaselist[item.ingredient.name][1] += item.value
    response = HttpResponse(content_type='application/pdf')
    content = 'attachment; filename="purchase_list.pdf"'
    response['Content-Disposition'] = content
    p = canvas.Canvas(response)
    for key, value in purchaselist.items():
        p.drawString(100, 100, '{} {} {}'.format(key, value[0], value[1]))
    p.showPage()
    p.save()
    return response


def about(request):
    return render(request, 'about.html')


def features(request):
    return render(request, 'features.html')
