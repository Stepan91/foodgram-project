from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.add_favorite, name='add_favorite'),
    path(
        'favorites/<int:recipe_id>/',
        views.del_favorite,
        name='del_favorite'
    ),
    path('purchases/', views.add_purchase, name='add_purchase'),
    path(
        'purchases/<int:recipe_id>/',
        views.del_purchase,
        name='del_purchase'
    ),
    path('ingredients/', views.ingredients_view,
         name='search_ingredients'),
    path(
        'subscriptions/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'subscriptions/<str:username>/',
        views.profile_unfollow,
        name='profile_unfollow'),
    path(
        '<str:username>/purchases/<int:recipe_id>/delete',
        views.delete_purchase,
        name='delete_purchase'
    )
]
