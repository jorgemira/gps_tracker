#!/usr/bin/env python3

import json
from datetime import datetime, timedelta
from decimal import Decimal
from json.decoder import JSONDecodeError
from time import sleep
from typing import Tuple, List

import requests
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from requests import RequestException

USERNAME = "asdfg"
PASSWORD = "asdfg"
HOST = "http://127.0.0.1:8000"
AUTH_PATH = "auth"
API_PATH = "api/locations"
SLEEP_TIME = 300  # 5 Min
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
# TODO: change to "/usr/local/share/gps_tracker/pending_locations.json"
PENDING_FILE = "pending_locations.json"
PRECISION = 6
R = Decimal(6373)
MIN_DISTANCE = Decimal(5000)


class GPSD:
    def __init__(self):
        self.gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

    def get_coordinates(self) -> Tuple[float, float, datetime]:
        """Get GPS coordinates as an average of the coordinates since last time it was collected"""
        time = datetime.utcnow().strftime(DATETIME_FORMAT)
        needed = {"lat", "lon", "time"}
        coords = {"lat", "lon"}
        lats = []
        lons = []

        location = self.gpsd.next()
        keys = set(location)

        while needed - keys or time > location.time:
            if not coords - keys:
                lats.append(location.lat)
                lons.append(location.lon)

            location = self.gpsd.next()
            keys = set(location)

        location_time = datetime.strptime(location.time, DATETIME_FORMAT)

        return self._avg(lats), self._avg(lons), location_time

    @staticmethod
    def _avg(items: List[float]) -> float:
        """Return the average value of a list of floats, by default it tries to compute it only with
        the items with a precision of at least PRECISION digits"""
        if not items:
            return 0

        filtered_items = [item for item in items if len(str(item).split(".")[1]) >= PRECISION]

        if len(filtered_items):
            items = filtered_items

        return sum(items) / len(items)


class Location:
    def __init__(self, longitude: Decimal, latitude: Decimal, datetime_: datetime):
        self.latitude = latitude
        self.longitude = longitude
        self.datetime_ = datetime_

    def to_json(self) -> str:
        decimals = Decimal(10) ** -PRECISION

        return json.loads(
            f'{{"latitude": {self.latitude.quantize(decimals)}, '
            f'"longitude": {self.longitude.quantize(decimals)}, '
            f'"datetime": "{self.datetime_.strftime(DATETIME_FORMAT)}"}}'
        )

    def append_failed_location(self) -> None:
        """Append location into PENDING_FILE"""
        with open(PENDING_FILE, "w+") as file:
            file.write(self.to_json() + "\n")

    @classmethod
    def from_json(cls, text) -> "Location":
        value = json.loads(text)

        return cls(
            Decimal(value["latitude"]),
            Decimal(value["longitude"]),
            datetime.strptime(value["datetime"], DATETIME_FORMAT)
        )

    @classmethod
    def acquire(cls, gpsd: GPSD) -> "Location":
        """Create a new Location object based on the GPS coordinates"""
        try:
            latitude, longitude, datetime_ = gpsd.get_coordinates()
        except Exception:
            raise ValueError("Couldn't get GPS coordinates")

        return cls(Decimal(latitude), Decimal(longitude), datetime_)


class Server:
    def __init__(self):
        self.token = None

    def login(self) -> None:
        """Get and store authentication token from server"""
        auth_url = f"{HOST}/{AUTH_PATH}/"
        contents = {"username": USERNAME, "password": PASSWORD}
        response = requests.post(auth_url, json=contents)
        if response.status_code != 200:
            raise ValueError("Invalid login credential")
        content = json.loads(response.content)
        self.token = content["token"]

    def post_location(self, location: Location) -> None:
        """Upload a location into the server"""
        if self.token is None:
            raise ValueError("Client not logged in")
        api_url = f"{HOST}/{API_PATH}/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.post(api_url, json=location.to_json(), headers=headers)
        # TODO: check what happens with date duplicates
        if response.status_code != 201:
            raise ValueError("Error when uploading location")

    def is_panic_mode(self) -> bool:
        url = f"{HOST}/{API_PATH}/panic"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(url, headers=headers)
        return response.content == b"true"


    def send_unsent_locations(self) -> bool:
        """Iterate through the list of locations that have not been sent and try to send them,
        store the ones that cannot be sent, return true if any location is still pending"""
        unsent_locations = self._get_unsent_locations()
        failed_locations = []

        for location in unsent_locations:
            try:
                self.post_location(location)
            except RequestException:
                failed_locations.append(location)

        self._write_failed_locations(failed_locations)

        return bool(failed_locations)

    @staticmethod
    def _get_unsent_locations() -> List[Location]:
        """Return a list of the locations that have not been sent"""
        locations = []

        with open(PENDING_FILE) as file:
            for line in file:
                try:
                    locations.append(Location.from_json(line))
                except JSONDecodeError:
                    print(f"Error decoding string: '{line}'")

        return locations

    @staticmethod
    def _write_failed_locations(failed_locations: List[Location]) -> None:
        """Write a list of locations into the PENDING_FILE"""
        with open(PENDING_FILE, "w") as file:
            file.write("\n".join((location.to_json()) for location in failed_locations))


def main() -> None:
    server = Server()
    failed_locations = True
    gpsd = GPSD()

    while True:
        sleep(SLEEP_TIME)

        if not server.token:
            try:
                server.login()
            except RequestException:
                pass

        if server.token:
            if failed_locations:
                failed_locations = server.send_unsent_locations()

            location = Location.acquire(gpsd)
            try:
                server.post_location(location)
            except RequestException:
                location.append_failed_location()
                failed_locations = True
        else:
            location = Location.acquire(gpsd)
            location.append_failed_location()
            failed_locations = True


if __name__ == '__main__':
    main()
