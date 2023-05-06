from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, SAFE_METHODS)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from recipes.models import Tag, Ingredient, Recipe, ShoppingCart, Favorites
from .filters import IngredientFilter, TagFilter
from .mixins import CreateDeleteViewSet
from .permissions import IsOwnerOrReadOnly
from .serializers import (SubscriptionSerializer, TagSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          RecipeEditSerializer, UserListSerializer,
                          ShoppingCartSerializer, FavoriteRecipeSerializer,
                          CreateUserSerializer)
from users.models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return CreateUserSerializer

        return UserListSerializer

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request},)

        return self.get_paginated_response(serializer.data)


class SubscriptionViewSet(CreateDeleteViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.user.subscriptions.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')

        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, user_id):
        get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(
                user=request.user, author_id=user_id).exists():
            return Response({'errors': 'На этого автора не было подписки'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Subscription,
            user=request.user,
            author_id=user_id
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filterset_class = IngredientFilter
    search_fields = ('^name', )


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filterset_class = TagFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer

        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        pagination_class=None)
    def download_file(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(
                'Корзина товаров пуста', status=status.HTTP_400_BAD_REQUEST)

        text = 'Список необходимых ингредиентов:\n\n'
        ingredient_name = 'recipe__recipe__ingredient__name'
        ingredient_unit = 'recipe__recipe__ingredient__measurement_unit'
        recipe_amount = 'recipe__recipe__amount'
        amount_sum = 'recipe__recipe__amount__sum'
        cart = user.shopping_cart.select_related('recipe').values(
            ingredient_name, ingredient_unit
        ).annotate(Sum(recipe_amount))
        for _ in cart:
            text += (
                f'{_[ingredient_name]} ({_[ingredient_unit]})'
                f' — {_[amount_sum]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class ShoppingCartViewSet(CreateDeleteViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return self.request.user.shopping_cart.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')

        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        user = request.user
        if not user.shopping_cart.select_related('recipe').filter(
                recipe_id=recipe_id
        ).exists():
            return Response({'errors': 'Такого рецепта нет в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeViewSet(CreateDeleteViewSet):
    serializer_class = FavoriteRecipeSerializer

    def get_queryset(self):
        return self.request.user.favorites.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')

        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe, id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        if not request.user.favorites.filter(recipe_id=recipe_id).exists():
            return Response({'errors': 'Этого рецепта и так нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Favorites,
            user=request.user,
            recipe_id=recipe_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
