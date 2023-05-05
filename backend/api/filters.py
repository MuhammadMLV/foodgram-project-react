from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Tag


class TagFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='isstartswith')
    slug = filters.CharFilter(lookup_expr='isstartswith')

    class Meta:
        model = Tag
        fields = ('name', 'slug')


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
