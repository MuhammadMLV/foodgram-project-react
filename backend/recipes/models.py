from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from core import constants

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LEN_RECIPE_NAME,
        unique=True
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=constants.HEX_LEN,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        )]
    )
    slug = models.CharField(
        'Слаг',
        unique=True,
        max_length=constants.MAX_LEN_RECIPE_NAME
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} - color:{self.color}'


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LEN_RECIPE_NAME,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.MAX_LEN_MEASUREMENT_UNIT
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LEN_RECIPE_NAME,
    )
    text = models.TextField(
        'Описание'
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        related_name='recipes',
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = models.ManyToManyField(
        verbose_name='Тэги',
        to=Tag,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        verbose_name='Ингредиенты',
        to=Ingredient,
        related_name='recipes',
        through='recipes.AmountIngredient',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipe_images/'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_author_recipe'
            ),
        ]

    def __str__(self):
        return f'{self.name}, автор: {self.author.username}'


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        to=Recipe,
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        verbose_name='Ингредиент',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                constants.MIN_INGREDIENT_AMOUNT,
                'Нужно хоть какое-то количество'
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} => {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        to=Recipe,
        related_name='recipe_shopping_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_shopping_cart')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user.username}, {self.recipe.name}'


class Favorites(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Избранный рецепт',
        to=Recipe,
        related_name='in_favorites',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Пользователя',
        to=User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(
        'Дата добавления в избранное',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('-date_added', )
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} => {self.recipe.name}'
