import json
from datetime import datetime
from decimal import Decimal

from . import constants as c


class Location:
    def __init__(self, longitude: Decimal, latitude: Decimal, datetime_: datetime):
        self.latitude = latitude
        self.longitude = longitude
        self.datetime_ = datetime_

    def to_json(self) -> str:
        decimals = Decimal(10) ** -c.PRECISION

        return json.loads(
            f'{{"latitude": {self.latitude.quantize(decimals)}, '
            f'"longitude": {self.longitude.quantize(decimals)}, '
            f'"datetime": "{self.datetime_.strftime(c.DATETIME_FORMAT)}"}}'
        )

    @classmethod
    def from_json(cls, text: str) -> "Location":
        value = json.loads(text)

        return cls(
            Decimal(value["latitude"]),
            Decimal(value["longitude"]),
            datetime.strptime(value["datetime"], c.DATETIME_FORMAT)
        )
