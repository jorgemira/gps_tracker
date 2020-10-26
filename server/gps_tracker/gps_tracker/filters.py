from django_filters import rest_framework as filters

from .models import Location


class LocationFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="datetime", lookup_expr="gte")
    max_date = filters.DateTimeFilter(field_name="datetime", lookup_expr="lte")
    show_all = filters.BooleanFilter(method="show_all_filter")

    def show_all_filter(self, queryset, value, *args, **kwargs):
        if args and args[0]:
            return queryset.all()
        else:
            return queryset.filter(hidden=False)

    class Meta:
        model = Location
        fields = []
