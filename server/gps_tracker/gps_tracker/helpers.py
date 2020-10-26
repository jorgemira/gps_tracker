import math
import os
from decimal import Decimal

PANIC_FILE = "panic_file"
R = 6371
MAX_DISTANCE = Decimal(5)


def is_panic() -> bool:
    return os.path.exists(PANIC_FILE)


def set_panic_mode(mode: bool) -> None:
    if mode:
        os.remove(PANIC_FILE)
    else:
        open(PANIC_FILE, "w").close()


def distance_coordinates(lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal) -> Decimal:
    """Calculate the distance between two coordinates using the Haversine formula"""
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = Decimal(R * c)

    return distance
