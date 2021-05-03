from rest_framework import serializers
from recipes.models import Ingredient
from api.models import Favorite, Purchase, Follow
from rest_framework.validators import UniqueTogetherValidator


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Purchase
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'unit']
        model = Ingredient
