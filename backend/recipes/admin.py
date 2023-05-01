from django.contrib import admin
from django.contrib.admin import register

from .models import (AmountIngredient, Favorites, Ingredient, Recipe,
                     ShoppingCart, Tag)


@register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    pass


@register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('id', 'user', 'recipe')


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = ('name', )
    list_filter = ('name', )


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'favorites_count',
    )
    search_fields = ('name', 'text')
    list_filter = (
        'name', 'tags__name', 'author__username',
    )

    def favorites_count(self, obj):
        return obj.in_favorites.count()

    favorites_countg.short_description = 'Добавили в избранное'


@register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug'
    )
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
