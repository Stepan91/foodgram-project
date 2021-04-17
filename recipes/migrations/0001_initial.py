# Generated by Django 3.1.3 on 2021-04-12 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('tag', models.CharField(choices=[('Завтрак', 'Breakfest'), ('Обед', 'Dinner'), ('Ужин', 'Supper')], max_length=7)),
                ('cooking_time', models.DecimalField(decimal_places=3, max_digits=10)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredient', models.ManyToManyField(through='recipes.IngredientList', to='recipes.Ingredient')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='ingredientlist',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
