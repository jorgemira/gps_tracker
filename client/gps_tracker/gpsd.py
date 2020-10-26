from datetime import datetime
from decimal import Decimal
from typing import Tuple, List

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE

from . import constants as c
from .location import Location


class GPSD:
    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

    @classmethod
    def get_location(cls) -> Location:
        """Create a new Location object based on the GPS coordinates"""
        latitude, longitude, datetime_ = GPSD._get_coordinates()
        return Location(latitude, longitude, datetime_)

    @classmethod
    def _get_coordinates(cls) -> Tuple[Decimal, Decimal, datetime]:
        """Get GPS coordinates as an average of the coordinates since last time it was collected"""
        time = datetime.utcnow().strftime(c.DATETIME_FORMAT)
        needed = {"lat", "lon", "time"}
        coords = {"lat", "lon"}
        lats = []
        lons = []

        location = cls.gpsd.next()
        keys = set(location)

        while needed - keys or time > location.time:
            if not coords - keys:
                lats.append(Decimal(location.lat))
                lons.append(Decimal(location.lon))

            location = cls.gpsd.next()
            keys = set(location)

        location_time = datetime.strptime(location.time, c.DATETIME_FORMAT)

        return cls._avg(lats), cls._avg(lons), location_time

    @staticmethod
    def _avg(items: List[Decimal]) -> Decimal:
        """Return the average value of a list of Decimals"""
        try:
            return sum(items) / len(items)
        except ZeroDivisionError:
            return Decimal(0)
