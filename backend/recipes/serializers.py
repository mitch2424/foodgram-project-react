from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the output of ingredients."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Serializer for a brief display of the recipe."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class ShowIngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for displaying ingredients in a recipe."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """A serializer for adding ingredients."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class AddRecipeSerializer(serializers.ModelSerializer):
    """Serializer for adding a recipe."""

    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(use_url=True, max_length=None)
    name = serializers.CharField(max_length=200)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
            "author",
        )

    def validate(self, ingredients_):
        """Validation of ingredients for creating a recipe"""

        if not ingredients_['ingredients'] or not ingredients_['tags']:
            raise ValidationError(
                '???????????????? ?????????????????????? ?? ?????????????? ?????? ?????? ??????????????!'
            )
        ingredients = ingredients_['ingredients']
        min_ingredients = 2
        if len(ingredients) < min_ingredients:
            raise ValidationError(
                '???????????????????????? ???????????? ???????? ?????? ?????? ????????????!'
            )
        data = []
        for ingredient in ingredients:
            data.append(ingredient['id'])
            if ingredient['amount'] <= 0:
                ingredient_incorrect = ingredient['id']
                raise ValidationError(
                    f'???? - ?????????????????????? "{ingredient_incorrect}" ????'
                    '???????????? ???????? ?????????? ???????? ?????? ?????????????????????????? ????????????!'
                )
        check_unique = set(data)
        if len(check_unique) != len(data):
            raise ValidationError(
                '?????????????????????? ??????????????????????, ???????????????????? ???? ?????? ???????????????? ????????????!'
            )
        if ingredients_['cooking_time'] <= 0:
            raise ValidationError(
                '?????????? ?????????????????????????? ???????????? ???????? ???????????? ????????!'
            )
        return ingredients_

    @staticmethod
    def __add_ingredients(ingredients, recipe):
        ingredients_to_add = [
            RecipeIngredient(
                ingredient=ingredient.get("id"),
                recipe=recipe,
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(ingredients_to_add)

    def create(self, validated_data):
        author = self.context.get("request").user
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        image = validated_data.pop("image")
        recipe = Recipe.objects.create(
            image=image, author=author, **validated_data
        )
        self.__add_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self.__add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        return ShowRecipeSerializer(
            recipe, context={"request": self.context.get("request")}
        ).data


class ShowRecipeSerializer(serializers.ModelSerializer):
    """Serializer for displaying the recipe."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "is_favorited",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_in_shopping_cart",
        )

    @staticmethod
    def get_ingredients(obj):
        """We get the ingredients from the RecipeIngredient model."""
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return ShowIngredientsInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        """Check whether the recipe is in the favorites."""
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj, user=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """We check whether the recipe is in the shopping cart."""
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj, user=request.user
        ).exists()


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Serializer of favorites."""

    user = serializers.HiddenField(
        default=CustomUserSerializer(read_only=True)
    )
    recipe = ShortRecipeSerializer(read_only=True)

    class Meta:

        model = FavoriteRecipe
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=("user", "recipe"),
                message="???????????? ?????? ?? ??????????????????",
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Shopping list serializer."""

    user = serializers.HiddenField(
        default=CustomUserSerializer(read_only=True)
    )
    recipe = ShortRecipeSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=("user", "recipe"),
                message="???????????? ?????? ?? ???????????? ??????????????",
            )
        ]
