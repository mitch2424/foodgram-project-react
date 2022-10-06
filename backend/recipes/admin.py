from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class BaseAdminSettings(admin.ModelAdmin):
    """Base admin panel."""
    empty_value_display = '-пусто-'
    list_filter = ('author', 'name', 'tags')


class IngredientRecipeInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели ингредиентов в рецепте.
    """
    model = IngredientRecipe
    extra = 0


class TagAdmin(BaseAdminSettings):
    """
    Custom admin panel (управление тегам).
    """
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(BaseAdminSettings):
    """
    Custom admin panel (управление ингредиентами).
    """
    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(BaseAdminSettings):
    """
    Custom admin panel (управление рецептами).
    """
    list_display = (
        'name',
        'author',
        'in_favorite'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('in_favorite',)
    filter_horizontal = ('tags',)
    inlines = (IngredientRecipeInline,)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()

    in_favorite.short_description = 'Количество добавлений в избранное'


class IngredientRecipeAdmin(admin.ModelAdmin):
    """
    Custom admin panel (управление ингридиентами в рецептах).
    """
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient')


class FavoriteAdmin(admin.ModelAdmin):
    """
    Custom admin panel (управление избранных рецептов).
    """
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


class CartAdmin(admin.ModelAdmin):
    """
    Custom admin panel (управление избранных рецептов).
    """
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
