from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

from .filters import LocationFilter
from .helpers import is_panic, distance_coordinates, MAX_DISTANCE
from .models import Location
from .serializers import LocationSerializer


class LocationCreateAPIView(ViewSetMixin, ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("datetime",)
    filterset_class = LocationFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        last_location = Location.objects.filter(hidden=False).order_by("-datetime").first()
        if last_location:
            distance = distance_coordinates(
                last_location.latitude,
                last_location.longitude,
                serializer.validated_data.get("latitude"),
                serializer.validated_data.get("longitude"),
            )
            hidden = distance < MAX_DISTANCE
        else:
            hidden = False

        serializer.save(hidden=hidden, panic=is_panic())


@api_view()
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def panic(request):
    return JsonResponse({"panic": is_panic()})
