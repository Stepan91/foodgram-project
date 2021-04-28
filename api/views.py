from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from recipes.models import Favorite, Purchase, Recipe, Ingredient
from .serializers import (
    FavoriteSerializer, PurchaseSerializer, IngredientSerializer
)

SUCCESS_TRUE = {'success': True}


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


@api_view(['DELETE'])
def del_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
    if favorite.exists():
        favorite.delete()
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


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
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


class IngredientsApiView(generics.ListAPIView):
    search_fields = ['title']
    filter_backends = [filters.SearchFilter]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
