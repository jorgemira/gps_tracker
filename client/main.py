#!/usr/bin/env python3

from time import sleep

import schedule

from gps_tracker import constants as c
from gps_tracker.jobs import panic_job, post_location_job, schedule_job
from gps_tracker.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    # Schedule jobs
    schedule_job(post_location_job, c.TIME_NO_PANIC)
    schedule_job(panic_job, c.TIME_CHECK_PANIC)

    # Run scheduled jobs
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
