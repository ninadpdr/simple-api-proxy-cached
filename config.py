# encoding=utf-8
# Author: ninadpage

# Logging
LOGFILE_DIR = 'logs/simple-api-proxy-cached/'
# When provisioned on a production server (and running as root or a user with sufficient permissions),
# this directory would be /var/log/...
LOGFILE_NAME = 'app-errors.log'

STDOUT_MAX_LOG_LEVEL = 'WARNING'            # All logs at or below this level to be logged on stdout
STDERR_MIN_LOG_LEVEL = 'ERROR'              # All logs at or above this level to be logged on stderr

FILE_LOG_LEVEL = 'ERROR'
CONSOLE_LOG_LEVEL = 'DEBUG'
DEFAULT_LOG_LEVEL = 'INFO'

# Response Caching
RESPONSE_CACHE_TIMEOUT = int(4.2*60)        # 4.2 minutes!

# API Token
API_TOKEN = '361c5f41768785098059ef77e71af8152dca12e4'

# HTTP status codes
HTTP_SUCCESS_CODES = [200, 201, 202, 203]
