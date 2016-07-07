# encoding=utf-8
# Author: ninadpage

from applogging import app_logger

from flask import Flask
from flask_restful import Api, got_request_exception

from resources.helloworld import HelloWorld


def log_traceback(sender, exception, **extra):
    app_logger.exception('Unhandled exception in {}:'.format(sender), exc_info=exception, **extra)


# Create the Flask app
application = Flask(__name__)
api = Api(application)

# Add exception handler for unhandled exceptions, which logs the traceback
got_request_exception.connect(log_traceback, application)

# Routing the endpoints to the right resources
api.add_resource(HelloWorld, '/')


# Start the app if this module is directly invoked
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
    # App runs in debug mode if invoked directly. In production, it would probably be sitting behind
    # a WSGI middleware (and nginx).
