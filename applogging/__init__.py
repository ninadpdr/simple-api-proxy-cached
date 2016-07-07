# encoding=utf-8
# Author: ninadpage

import os
import sys
import logging
import logging.config

import config


def _get_stderr_log_level():
    # Returns log level for stderr handler: max of CONSOLE_LOG_LEVEL & STDERR_MIN_LOG_LEVEL.
    # e.g., if you want to only see CRITICAL logs on console while running the app, you only need to change
    # CONSOLE_LOG_LEVEL, and this method will take care choosing of correct level for stderr handler.
    console_log_level = logging._nameToLevel[config.CONSOLE_LOG_LEVEL]
    stderr_min_log_level = logging._nameToLevel[config.STDERR_MIN_LOG_LEVEL]
    stderr_log_level = max(console_log_level, stderr_min_log_level)
    return logging.getLevelName(stderr_log_level)


logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'extended': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        },
    },
    'filters': {
        'maxlevelfilter': {
            '()': 'applogging.filters.MaxLevelFilter',
            'max_level': config.STDOUT_MAX_LOG_LEVEL,
        }
    },
    'handlers': {
        'file': {
            'level': config.FILE_LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'extended',
            'filename': os.path.join(config.LOGFILE_DIR, config.LOGFILE_NAME),
            'when': 'midnight',
            'backupCount': 30,
        },
        'stdout': {
            'level': config.CONSOLE_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'extended',
            'filters': ['maxlevelfilter'],
            'stream': sys.stdout,
        },
        'stderr': {
            'level': _get_stderr_log_level(),
            'class': 'logging.StreamHandler',
            'formatter': 'extended',
            'stream': sys.stderr,
        },
    },
    # Logger names should always start with a common prefix. It helps when you are emitting logs to a distributed
    # stack (e.g. ELK). You can apply a filter "name=prefix*", which will show all logs coming from this
    # service. If you want to see logs from only a particular request handler (e.g. events handler), you can
    # then apply a specific filter (name="apiproxy-eventshandler").
    'loggers': {
        'apiproxy-app': {
            'handlers': ['file', 'stdout', 'stderr'],
            'level': config.DEFAULT_LOG_LEVEL,
        },
        'apiproxy-eventshandler': {
            'handlers': ['file', 'stdout', 'stderr'],
            'level': config.DEFAULT_LOG_LEVEL,
        },
        'apiproxy-requestsmanager': {
            'handlers': ['file', 'stdout', 'stderr'],
            'level': config.DEFAULT_LOG_LEVEL,
        },
    },
}


# Create log file directory (including parent directories) if it doesn't exist
os.makedirs(config.LOGFILE_DIR, exist_ok=True)


# Configure loggers
logging.config.dictConfig(logging_config)


# Initialize module level variables
app_logger = logging.getLogger('apiproxy-app')
eventshandler_logger = logging.getLogger('apiproxy-eventshandler')
requestsmanager_logger = logging.getLogger('apiproxy-requestsmanager')
