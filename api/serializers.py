from rest_framework import serializers
from recipes.models import Favorite, Purchase, Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient
