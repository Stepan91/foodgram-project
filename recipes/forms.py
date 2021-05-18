from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'title',
            'tag',
            'cooking_time',
            'description',
            'image')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(),
        }
        labels = {
            'title': 'Название рецепта',
            'tag': 'Теги',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить изображение'
        }
