from typing import Callable

import schedule

from . import constants as c
from .gpsd import GPSD
from .logging import get_logger
from .server import Server

logger = get_logger(__name__)


def schedule_job(job: Callable, seconds: int) -> None:
    """Clear a previously running job, if exists, and launch it again"""
    schedule.clear(job.__name__)
    job()
    schedule.every(seconds).seconds.do(job).tag(job.__name__)


def post_location_job() -> None:
    """Post unsent location list and then post current location"""
    if not Server.token:
        Server.login()

    try:
        location = GPSD.get_location()
    except Exception:
        logger.exception("Cannot acquire location")
        return

    if Server.token:
        Server.send_unsent_locations()
        Server.post_location(location)
    else:
        Server.append_failed_location(location)


def panic_job() -> None:
    """Check for panic mode and reschedule post_location_job if necesary"""
    new_panic = Server.is_panic_mode()

    if Server.panic_mode and not new_panic:
        logger.info("Disabling panic mode")
        schedule_job(post_location_job, c.TIME_NO_PANIC)
    elif not Server.panic_mode and new_panic:
        logger.info("Enabling panic mode")
        schedule_job(post_location_job, c.TIME_PANIC)

    Server.panic_mode = new_panic
