from django.contrib import admin

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    AmountIngredient,
)


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "amount",)
    list_filter = ("ingredient",)

    @admin.display(description="Ингредиенты")
    def get_ingredients(self, obj):
        return '\n'.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f'{item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "amount_favorites")
    list_filter = ("name", "author", "tags")
    search_fields = ("name",)
    empty_value_display = "-пусто-"

    @staticmethod
    @admin.display(description="В избранном, раз")
    def amount_favorites(obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "ingredient",
        "amount",
    )
    list_filter = ("id", "recipe", "ingredient")
    empty_value_display = "-пусто-"


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("user",)
