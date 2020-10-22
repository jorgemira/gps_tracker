#!/usr/bin/env python3

import datetime as dt
from decimal import Decimal
import json
from json.decoder import JSONDecodeError
from time import sleep
from typing import Tuple, List

import requests
from requests import RequestException
# from gps import gps, WATCH_ENABLE , WATCH_NEWSTYLE


USERNAME = "asdfg"
PASSWORD = "asdfg"
HOST = "http://127.0.0.1:8000"
AUTH_PATH = "auth"
API_PATH = "api/locations"
SLEEP_TIME = 300  # 5 Min
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# TODO: change to "/usr/local/share/gps_tracker/pending_locations.json"
PENDING_FILE = "pending_locations.json"
PRECISION = 6


def get_coordinates() -> Tuple[float, float]:
    # TODO: change to real gps stuff
    #   nx = gpsd.next()
    #   return nx.lat, nx.lon
    return 1.2, 4.5


class Location:
    def __init__(self, longitude: Decimal, latitude: Decimal, datetime: dt.datetime):
        self.latitude = latitude
        self.longitude = longitude
        self.datetime = datetime

    def to_json(self) -> str:
        decimals = Decimal(10) ** -PRECISION
        return json.loads(
            f'{{"latitude": {self.latitude.quantize(decimals)}, '
            f'"longitude": {self.longitude.quantize(decimals)}, '
            f'"datetime": "{self.datetime.strftime(DATETIME_FORMAT)}"}}'
        )

    @classmethod
    def from_json(cls, text) -> "Location":
        value = json.loads(text)
        return cls(
            Decimal(value["latitude"]),
            Decimal(value["longitude"]),
            dt.datetime.strptime(value["datetime"], DATETIME_FORMAT)
        )

    @classmethod
    def acquire(cls) -> "Location":
        try:
            lat, long = get_coordinates()
        except Exception:
            raise ValueError("Couldn't get GPS coordinates")

        return cls(Decimal(lat), Decimal(long), dt.datetime.now())


class Server:
    def __init__(self):
        self.token = None

    def login(self):
        auth_url = f"{HOST}/{AUTH_PATH}/"
        contents = {"username": USERNAME, "password": PASSWORD}
        response = requests.post(auth_url, json=contents)
        if response.status_code != 200:
            raise ValueError("Invalid login credential")
        content = json.loads(response.content)
        self.token = content["token"]

    def post_location(self, location: Location) -> None:
        if self.token is None:
            raise ValueError("Client not logged in")
        api_url = f"{HOST}/{API_PATH}/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.post(api_url, json=location.to_json(), headers=headers)
        # TODO: check what happens with date duplicates
        if response.status_code != 201:
            raise ValueError("Error when uploading location")


def send_unsent_locations(server: Server) -> bool:
    unsent_locations = get_unsent_locations()
    failed_locations = []

    for location in unsent_locations:
        try:
            server.post_location(location)
        except RequestException:
            failed_locations.append(location)

    write_failed_locations(failed_locations)

    return bool(failed_locations)


def get_unsent_locations() -> List[Location]:
    locations = []
    with open(PENDING_FILE) as file:
        for line in file:
            try:
                locations.append(Location.from_json(line))
            except JSONDecodeError:
                print(f"Error decoding string: '{line}'")
    return locations


def write_failed_locations(failed_locations: List[Location]) -> None:
    with open(PENDING_FILE, "w") as file:
        file.write("\n".join((location.to_json()) for location in failed_locations))


def append_failed_location(location: Location) -> None:
    with open(PENDING_FILE, "w+") as file:
        file.write(location.to_json() + "\n")


def main():
    server = Server()
    failed_locations = True

    while True:
        if not server.token:
            try:
                server.login()
            except RequestException:
                pass

        if server.token:
            if failed_locations:
                failed_locations = send_unsent_locations(server)

            location = Location.acquire()
            try:
                server.post_location(location)
            except RequestException:
                append_failed_location(location)
                failed_locations = True
        else:
            location = Location.acquire()
            append_failed_location(location)
            failed_locations = True

        sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
