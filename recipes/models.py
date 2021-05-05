from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator

User = get_user_model()

TAG_CHOICES = [
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
    ]


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ингредиент')
    unit = models.CharField(max_length=50, verbose_name='Ед. изм.')

    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты')
    tag = MultiSelectField(
        verbose_name='Теги',
        choices=TAG_CHOICES,
        max_choices=3,
        default='Обед'
    )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Рецепт')
    value = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент-Рецепт'
        verbose_name_plural = 'Ингредиенты-Рецепты'
