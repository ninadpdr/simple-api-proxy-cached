# encoding=utf-8
# Author: ninadpage

from flask_restful import Resource
import requests.exceptions

from applogging import eventshandler_logger
from resources.common.api_requests_manager import get_request, APIReturnedError


def create_error_tuple(message, http_code=400):
    return {
        'error': {
            'message': message,
            'status_code': http_code,
        }
    }, http_code


class EventsWithSubscription(Resource):
    """
    Given an event ID, returns the event title and the first names of its attendees.
    """

    def get(self, event_id):
        try:
            event_details = get_request('https://demo.calendar42.com/api/v2/events/{event_id}/'.format(
                event_id=event_id)).json()
            if event_details['meta_data']['count'] < 1:
                return create_error_tuple('Invalid event ID', 400)
            event_title = event_details['data'][0]['title']

            event_subscriptions = get_request(
                'https://demo.calendar42.com/api/v2/event-subscriptions/',
                params={'event_ids': '[event_id]'.format(event_id=event_id)}
            ).json()
            # Extract first names of the subscriber from the list of event subscriptions
            first_names = [subscription['subscriber']['first_name'] for subscription in event_subscriptions['data']]

            return {
                'id': event_id,
                'title': event_title,
                'names': first_names,
            }, 200

        except requests.exceptions.Timeout:
            return create_error_tuple('Connection to target server timed out', 504)

        except requests.exceptions.RequestException:
            return create_error_tuple('Bad response from target server', 502)

        except APIReturnedError as e:
            # Ideally, here we should distinguish between 'expected' errors (e.g. 404 when user-provided event_id is
            # not found) and 'unexpected' errors (e.g. 400), based on target API specifications.
            # We should only forward the response of expected errors. Unexpected errors should be logged &
            # only a generic error message should be returned.
            response = e.response.json()
            return response, response['error']['status_code']

        except (ValueError, KeyError) as e:
            eventshandler_logger.error(
                'Invalid JSON returned by target server. event_id={}, error={}'.format(event_id, e))
            return create_error_tuple('Invalid response from target server', 502)

        # 400 response for bad input is handled by Flask-RESTful as we've specified the parameters &
        # their types in the routes

        except Exception as e:
            eventshandler_logger.exception(
                'Unhandled exception in events-with-subscription handler. event_id={}'.format(event_id),
                exc_info=e)
            return create_error_tuple('We hate to admit that we did not see this coming', 500)
