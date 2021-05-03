from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('purchaselist/get/', views.purchase_list, name='purchaselist'),
    path(
        '<str:username>/follow/',
        views.follow_index,
        name='follow_index'
    ),
    path(
        '<str:username>/favorites/',
        views.favorites_view,
        name='favorites_view'
    ),
    path(
        '<str:username>/purchases/',
        views.purchases_view,
        name='purchases_view'
    ),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='edit_recipe'
    ),
    path(
        '<str:username>/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='delete_recipe'
    ),
    path('<str:username>/', views.profile, name='profile')
]
