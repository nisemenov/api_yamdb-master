from django_filters.rest_framework import FilterSet, CharFilter
from review.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = CharFilter(field_name='category__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['year']
