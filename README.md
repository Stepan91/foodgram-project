![alt text](https://github.com/Stepan91/foodgram-project/actions/workflows/main.yml/badge.svg)
# Foodgram-project
#### ~~https://recipesocialnetwork.tk/~~
## Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.

## Стек технологий:
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- nginx
- Gunicorn
- GitHub Actions

## Запуск проекта, используя Docker (база данных PostgreSQL):
1. Клонируйте репозиторий с проектом:

       git clone https://github.com/Stepan91/foodgram-project.git

2. В директории проекта создайте файл .env, по пути <project_name>/foodgram/.env, в котором пропишите следующие параметры окружения:

       DATABASE_URL=psql://foodgram_user:foodgram@127.0.0.1:5432/foodgram

- имя пользователя с правами администратора для базы данных = foodrgam_user
- имя базы данных = foodgram

3. С помощью Dockerfile и docker-compose.yaml разверните проект:

       docker-compose up --build

Автоматически были созданы миграции для приложения и произошла миграция в базе данных. В базу данных загружены ингредиенты.

Проект запустился на http://127.0.0.1/

Аккаунт суперпользователя:
http://127.0.0.1/admin/
- username: admin
- password: admin
