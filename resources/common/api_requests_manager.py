# encoding=utf-8
# Author: ninadpage

# Defines HTTP requests handlers which send the requests using requests module. Includes Authorization header.
# In case of any exceptions, a traceback is logged and the exception is re-raised from it, so that
# the entire traceback is available for the caller.

import requests
import requests.exceptions

from applogging import requestsmanager_logger
import config


class APIReturnedError(Exception):
    """
    Custom Exception type for API errors. Also provides __str__ implementation which describes the error.
    """

    def __init__(self, response, *args, **kwargs):
        """
        Constructs APIReturnedError exception object.

        :param response: response object returned by the API
        :type response: requests.models.Response
        :param args: passed on to Exception constructor
        :param kwargs: passed on to Exception constructor
        """
        self.response = response
        super().__init__(*args, **kwargs)

    def __str__(self):
        error_msg = 'API returned error.\nURL: {}\nHTTP Response: {} {}'.format(
            self.response.url, self.response.status_code, self.response.reason)
        try:
            response_json = self.response.json()
            if 'error' in response_json:
                error_msg += '\nerror: {}'.format(response_json['error'])
        except ValueError:
            # No JSON in response, cannot extract further info about errors.
            error_msg += '\ntext: {}'.format(self.response.text)
        return error_msg


def get_request(url, params=None, **kwargs):
    # Adds Authorization header only if kwargs doesn't pass any headers. If kwargs does include headers, they override
    # any headers added by this method.
    try:
        if 'headers' not in kwargs:
            kwargs['headers'] = {'Authorization': 'Token {}'.format(config.API_TOKEN)}
        response = requests.get(url, params=params, **kwargs)
        if response.ok:
            return response
        raise APIReturnedError(response)
    except requests.exceptions.RequestException as e:
        requestsmanager_logger.exception('Exception in sending GET request to url={}'.format(url))
        raise
    except APIReturnedError as e:
        requestsmanager_logger.error(e)
        raise
