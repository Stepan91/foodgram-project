from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from recipes.models import Recipe, Ingredient, User
from .models import Favorite, Purchase, Follow
from .serializers import (
    FavoriteSerializer, PurchaseSerializer,
    IngredientSerializer, FollowSerializer
)

SUCCESS_TRUE = {'success': True}
SUCCESS_FALSE = {'success': False}


@login_required
@api_view(['POST'])
def add_favorite(request):
    id = int(request.data['id'])
    data = {'user': request.user.id, 'recipe': id}
    serializer = FavoriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['DELETE'])
def del_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
    if favorite.exists():
        favorite.delete()
        return Response(SUCCESS_TRUE, status=status.HTTP_200_OK)
    return Response(SUCCESS_FALSE, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_purchase(request):
    id = int(request.data['id'])
    data = {'user': request.user.id, 'recipe': id}
    serializer = PurchaseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def del_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    if purchase.exists():
        purchase.delete()
        return Response(SUCCESS_TRUE, status=status.HTTP_200_OK)
    return Response(SUCCESS_FALSE, status=status.HTTP_404_NOT_FOUND)


@login_required
def delete_purchase(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    if purchase.exists():
        purchase.delete()
    return redirect('purchases_view', username=request.user)


@login_required
@api_view(['POST'])
def profile_follow(request):
    author_name = request.data['id']
    author = User.objects.get(username=author_name)
    data = {'user': request.user.id, 'author': author.id}
    serializer = FollowSerializer(data=data)
    if request.user != author:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_404_NOT_FOUND)


@login_required
@api_view(['DELETE'])
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    relation = Follow.objects.filter(user=request.user, author=author)
    if relation.exists():
        relation.delete()
        return Response(SUCCESS_TRUE, status=status.HTTP_200_OK)
    return Response(SUCCESS_FALSE, status=status.HTTP_404_NOT_FOUND)


class IngredientsApiView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]
