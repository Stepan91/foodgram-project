from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Recipe, User, TAG_CHOICES
from .forms import RecipeForm
from .utils import save_recipe
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Q
from functools import reduce
from django.db.models import Sum
from .tags_instanse import TAGS_DICT
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


def generate_tags_list(tags: list):
    tag_list = [TAGS_DICT[tag] for tag in tags]
    return tag_list


def index(request):
    tags_instance = [i[0] for i in TAG_CHOICES]
    tags, tags_filter = get_tags(request)
    tag_list = generate_tags_list(tags_instance)
    if tags_filter:
        recipe_list = Recipe.objects.filter(tags_filter).all()
    else:
        recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
            'tag_list': tag_list,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'tags_instance': tags_instance
    }
    return render(request, 'index.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        save_recipe(request, form)
        return redirect('index')
    return render(request, 'new_edit_recipe.html', {'form': form})


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
        'new_edit_recipe.html',
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
    return render(
        request,
        'profile.html', {
            'page': page,
            'paginator': paginator,
            'author': author,
            'tags': tags,
            }
        )


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    if recipe.author == request.user:
        recipe.delete()
    return redirect('profile', username=username)


@login_required
def follow_index(request, username):
    authors = User.objects.filter(following__user__username=username)
    paginator = Paginator(authors, 3)
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
    recipe_list = Recipe.objects.filter(purchases__user__username=username)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'shoplist.html',
        {'page': page, 'paginator': paginator}
    )


def purchase_list(request):
    ingredients = request.user.purchases.values(
        'recipe__title',
        'recipe__ingredientrecipe__value',
        'recipe__ingredient__unit'
    ).annotate(
        amount=Sum('recipe__ingredientrecipe__value')
    )
    response = HttpResponse(content_type='application/pdf')
    content = 'attachment; filename="purchase_list.pdf"'
    response['Content-Disposition'] = content
    p = canvas.Canvas(response)
    for value in ingredients:
        p.drawString(100, 100, '{}'.format(value))
    p.showPage()
    p.save()
    return response


def about(request):
    return render(request, 'about.html')


def features(request):
    return render(request, 'features.html')
