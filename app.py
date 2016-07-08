# encoding=utf-8
# Author: ninadpage

from applogging import app_logger

from flask import Flask, request
from flask_restful import Api, got_request_exception
from werkzeug.contrib.cache import SimpleCache

import config
from resources.helloworld import HelloWorld
from resources.events_with_subscription import EventsWithSubscription


def log_traceback(sender, exception, **extra):
    app_logger.exception('Unhandled exception in {}:'.format(sender), exc_info=exception, **extra)


# Create the Flask app
app = Flask(__name__)
api = Api(app)

# Add exception handler for unhandled exceptions, which logs the traceback
got_request_exception.connect(log_traceback, app)

# Set up caching
# We are using SimpleCache, which will store the results in memory. For production, we'd probably be using memcached.
response_cache = SimpleCache()


# Lookup cache before every request is processed.
# If response is found in cache, return it without going to request handler.
@app.before_request
def return_cached():
    # if GET and POST not empty
    if not request.values:
        response = response_cache.get(request.path)
        if response:
            return response


# Store response in cache (with timeout) after every request is processed successfully by its handler.
@app.after_request
def cache_response(response):
    if not request.values and response.status_code in config.HTTP_SUCCESS_CODES:
        response_cache.set(request.path, response, config.RESPONSE_CACHE_TIMEOUT)
        # Set Cache-Control header
        response.cache_control.max_age = config.RESPONSE_CACHE_TIMEOUT
    return response


# Routing the endpoints to the right resources
api.add_resource(HelloWorld, '/')
api.add_resource(EventsWithSubscription, '/events-with-subscriptions/<string:event_id>/')


# Start the app if this module is directly invoked
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # App runs in debug mode if invoked directly. In production, it would probably be sitting behind
    # a WSGI middleware (and nginx).
