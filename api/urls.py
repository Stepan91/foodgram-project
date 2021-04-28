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
    path('ingredients/', views.IngredientsApiView.as_view(),
         name='search_ingredients')
]
