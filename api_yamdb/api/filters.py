import django_filters

from reviews.models import Title


class TitleFilters(django_filters.rest_framework.FilterSet):
    """
    Класс фильтрации полей модели Title для TitleViewSet
    """
    genre = django_filters.rest_framework.AllValuesFilter(
        field_name='genre__slug'
    )
    category = django_filters.rest_framework.AllValuesFilter(
        field_name='category__slug'
    )
    name = django_filters.rest_framework.AllValuesFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Title
        fields = [
            'genre',
            'category',
            'year',
            'name'
        ]
