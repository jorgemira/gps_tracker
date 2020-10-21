from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ViewSetMixin

from .models import Location
from .serializers import LocationSerializer
from .filters import LocationFilter


class LocationCreateAPIView(ViewSetMixin, ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("datetime",)
    filterset_class = LocationFilter
