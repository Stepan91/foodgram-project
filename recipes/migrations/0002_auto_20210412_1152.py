# Generated by Django 3.1.3 on 2021-04-12 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientlist',
            name='value',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.CharField(choices=[('Breakfast', 'Завтрак'), ('Dinner', 'Обед'), ('Supper', 'Ужин')], max_length=9),
        ),
    ]