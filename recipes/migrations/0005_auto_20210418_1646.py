# Generated by Django 3.1.7 on 2021-04-18 13:46

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210418_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Завтрак', 'Завтрак'), ('Обед', 'Обед'), ('Ужин', 'Ужин')], default='Обед', max_length=17),
        ),
    ]
