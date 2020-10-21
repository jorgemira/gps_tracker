from django_filters import rest_framework as filters

from .models import Location


class LocationFilter(filters.FilterSet):
    min_datetime = filters.DateTimeFilter(field_name="datetime", lookup_expr="gte")
    max_datetime = filters.DateTimeFilter(field_name="datetime", lookup_expr="lte")

    class Meta:
        model = Location
        fields = ["datetime"]