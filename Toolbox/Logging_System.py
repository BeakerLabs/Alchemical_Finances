"""
This script collects traceback errors and Developer set exceptions to help with debugging and error tracking.

Future Concepts
1) Separate out a Debug and Error level errors. This will require designating errors accordingly.
"""
#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import logging
import sys

from logging.handlers import TimedRotatingFileHandler
from os import path

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def create_log_fileName(sessionCount: int):
    from datetime import datetime
    date = datetime.now()
    date = date.strftime("%Y%m%d")
    date_str = str(date)

    sessionCount = str(sessionCount)

    filename = f"{date_str}S{sessionCount}_ErrorLog.txt"
    # Determining the pathway for the file should be done externally
    return filename


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # The logger will collect all exceptions above the set value.
    # NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(log_file))
    logger.propagate = False
    return logger
