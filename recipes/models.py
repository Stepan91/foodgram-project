from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    TAG_CHOICES = [
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes")
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    image = models.ImageField()
    description = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through='IngredientList')
    tag = models.CharField(max_length=9, choices=TAG_CHOICES)
    cooking_time = models.CharField(max_length=10)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-pub_date",)


class IngredientList(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=1)
