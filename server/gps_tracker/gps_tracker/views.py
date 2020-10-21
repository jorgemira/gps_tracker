from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ViewSetMixin

from .models import Location
from .serializers import LocationSerializer


class LocationCreateAPIView(ViewSetMixin, ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
