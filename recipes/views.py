from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import (
    Recipe, User, IngredientRecipe, Follow, Favorite, 
    Purchase, Ingredient
)
from .forms import RecipeForm
from .utils import save_recipe
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    relation = IngredientRecipe.objects.filter(
        recipe=recipe,
        )
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
        {'form': form, 'relation': relation, 'recipe': recipe}
    )


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    favorite = Favorite.objects.filter(recipe=recipe)
    purchase = Purchase.objects.filter(recipe=recipe)
    relation = IngredientRecipe.objects.filter(
        recipe=recipe,
        )
    form = RecipeForm()
    following = None
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author).exists()
    return render(
        request,
        'single_recipe.html',
        {
            'recipe': recipe,
            'author': recipe.author,
            'relation': relation,
            'form': form,
            'following': following,
            'favorite': favorite,
            'purchase': purchase
            }
        )


def profile(request, username):
    author = get_object_or_404(User, username=username)
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
            }
        )


@login_required
def recipe_delete(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = Recipe.objects.filter(author=author, id=recipe_id)
    if recipe.exists():
        recipe.delete()
    return redirect('profile', username=username)


@login_required
def follow_index(request):
    authors = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator
        }
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    relation = Follow.objects.filter(user=request.user, author=author)
    if relation.exists():
        relation.delete()
    return redirect('profile', username=username)


@login_required
def favorites_view(request, username):
    favorites = Favorite.objects.filter(user__username=username)
    recipe_list = Recipe.objects.filter(favorites__in=favorites)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorites.html',
        {'page': page, 'paginator': paginator}
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
        {'page': page, 'paginator': paginator}
    )


@login_required
def delete_purchase(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    if purchase.exists():
        purchase.delete()
    return redirect(
        'purchases_view',
        username=username
    )


def filter_tags(request, tag):
    recipe_list = Recipe.objects.filter(tag__contains=tag)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def filter_tags_favorite(request, username, tag):
    favorites = Favorite.objects.filter(user__username=username)
    recipe_list = Recipe.objects.filter(
        favorites__in=favorites,
        tag__contains=tag
    )
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorites.html',
        {'page': page, 'paginator': paginator}
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
    response[
        'Content-Disposition'
        ] = 'attachment; filename="purchase_list.pdf"'
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
