# REST API server related constants
USERNAME = "asdfg"
PASSWORD = "asdfg"
HOST = "http://127.0.0.1:8000"
AUTH_URL: str = f"{HOST}/auth/"
LOCATIONS_URL: str = f"{HOST}/api/locations/"
PANIC_URL: str = f"{HOST}/api/panic/"


# Format constants
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
PRECISION = 6

# Job scheduling constants
TIME_PANIC = 1  # TODO: Change to 60
TIME_NO_PANIC = 5  # TODO: Change to 1800
TIME_CHECK_PANIC = 3  # TODO: Change to 300

# Logging constants
LOG_FILE = "gps_tracker.log"  # TODO: move to  /var/log/
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

PENDING_FILE = "pending_locations.json"  # TODO: move to /usr/local/share/gps_tracker/
