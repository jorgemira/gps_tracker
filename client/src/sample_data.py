from datetime import datetime, timedelta
from decimal import Decimal

from .location import Location
from .server import Server

# TODO: add more data
SAMPLE_DATA = [
    [-0.510864, 38.333039],
    [0.054932, 38.706946],
    [-0.307617, 39.185433],
    [-0.060425, 39.981329],
    [0.582275, 40.713956],
    [1.230469, 41.10833],
    [2.04895, 41.467428],
    [2.988281, 42.269179],
]


def create_sample_data() -> None:
    server = Server()
    server.login()

    dt = datetime.utcnow() - timedelta(days=2)
    for (lon, lat) in SAMPLE_DATA:
        dt += timedelta(minutes=30)
        loc = Location(Decimal(lon), Decimal(lat), dt)
        server.post_location(loc)


if __name__ == '__main__':
    create_sample_data()
