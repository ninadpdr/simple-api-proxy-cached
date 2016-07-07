# encoding=utf-8
# Author: ninadpage

import logging


class MaxLevelFilter(logging.Filter):
    """
    Filters (lets through) all messages with level <= mex_level
    Useful, for example, if you want all CRITICAL & ERROR logs to go to stderr, and rest of the logs *excluding*
    ERROR & CRITICAL logs to go to stdout.
    In such case, you can create a handler for stderr with level ERROR, and another handler for stdout with level DEBUG
    and this filter with max_level=WARNING.
    """

    def __init__(self, max_level):
        super().__init__()
        self.max_level = logging._nameToLevel[max_level]

    def filter(self, record):
        return record.levelno <= self.max_level
