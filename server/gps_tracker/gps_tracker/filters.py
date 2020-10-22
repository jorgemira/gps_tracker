from django.db.models import Min
from django.db.models.functions import TruncDate, TruncHour
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from .models import Location


class LocationFilter(filters.FilterSet):
    min_datetime = filters.DateTimeFilter(field_name="datetime", lookup_expr="gte")
    max_datetime = filters.DateTimeFilter(field_name="datetime", lookup_expr="lte")
    frequency = filters.CharFilter(method="freq")

    def freq(self, queryset, value, *args, **kwargs):
        if args:
            if args[0] == "daily":
                trunc = TruncDate
            elif args[0] == "hourly":
                trunc = TruncHour
            else:
                raise ValidationError("Invalid frequency")
            firsts = {(Location.objects.values(dt=trunc("datetime"))
                       .annotate(firsts=Min("datetime")).values_list("firsts", flat=True))}
            queryset = queryset.filter(datetime__in=firsts)

        return queryset

    class Meta:
        model = Location
        fields = ["datetime"]
