import json
import os
from json.decoder import JSONDecodeError
from typing import List, Union

import requests
from requests import RequestException

from . import constants as c
from .location import Location
from .logging import get_logger

logger = get_logger(__name__)


class Server:
    token: Union[str, None] = None
    panic: bool = False
    auth_url: str = f"{c.HOST}/{c.AUTH_PATH}/"
    api_url: str = f"{c.HOST}/{c.API_PATH}/"
    panic_url: str = f"{c.HOST}/{c.API_PATH}/panic"  # TODO: change me
    panic_mode: bool = False

    @classmethod
    def login(cls) -> None:
        """Get and store authentication token from server"""
        contents = {"username": c.USERNAME, "password": c.PASSWORD}
        try:
            response = requests.post(cls.auth_url, json=contents)
            if response.status_code != 200:
                raise ValueError
            content = json.loads(response.content)
            cls.token = content["token"]
        except (RequestException, JSONDecodeError, ValueError):
            logger.exception("Error logging into server")
            cls.token = None

    @classmethod
    def post_location(cls, location: Location) -> None:
        """Upload a location into the server"""
        headers = {"Authorization": f"Token {cls.token}"}
        data = location.to_json()
        try:
            response = requests.post(cls.api_url, json=data, headers=headers)
            if response.status_code != 201:
                raise ValueError
        except (RequestException, ValueError):
            logger.exception("Error posting location")
            cls.append_failed_location(location)

    @classmethod
    def is_panic_mode(cls) -> bool:
        headers = {"Authorization": f"Token {cls.token}"}
        try:
            response = requests.get(cls.panic_url, headers=headers)
            content = json.loads(response.content)
            return content["panic"]
        except (RequestException, JSONDecodeError):
            logger.exception("Cannot get panic mode")
            return False

    @staticmethod
    def append_failed_location(location: Location) -> None:
        """Append location into PENDING_FILE"""
        try:
            with open(c.PENDING_FILE, "w+") as file:
                file.write(location.to_json() + "\n")
        except IOError:
            logger.exception("Cannot append failed location")

    @classmethod
    def send_unsent_locations(cls) -> None:
        """Iterate through the list of locations that have not been sent and try to send them"""
        unsent_locations = cls._get_unsent_locations()

        for location in unsent_locations:
            cls.post_location(location)

    @staticmethod
    def _get_unsent_locations() -> List[Location]:
        """Return a list of the locations that have not been sent"""
        locations = []

        if not os.path.exists(c.PENDING_FILE):
            return locations

        with open(c.PENDING_FILE) as file:
            for line in file:
                try:
                    locations.append(Location.from_json(line))
                except JSONDecodeError:
                    logger.warn(f"Error decoding string: '{line}'")

        os.remove(c.PENDING_FILE)

        return locations
