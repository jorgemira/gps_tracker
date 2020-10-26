import logging
from logging.handlers import TimedRotatingFileHandler

from . import constants as c


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter(c.LOG_FORMAT)

    log_file_handler = TimedRotatingFileHandler(filename=c.LOG_FILE, when="midnight")
    streamhandler = logging.StreamHandler()

    for handler in (log_file_handler, streamhandler):
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    return logger
