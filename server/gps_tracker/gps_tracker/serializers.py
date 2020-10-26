from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ")
    panic = serializers.ReadOnlyField()
    hidden = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ("latitude", "longitude", "datetime", "panic", "hidden")
