from django.contrib import admin
from .models import Follow, Favorite, Purchase


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
