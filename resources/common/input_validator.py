# encoding=utf-8
# Author: ninadpage

from collections import defaultdict


class RequestErrorReport(object):

    def __init__(self, request_dict):
        self.request_dict = request_dict
        self.errors = defaultdict(list)

    # Allows `if error_report: ...`
    def __bool__(self):
        return bool(self.errors)

    def __str__(self):
        return 'Request: {}\nRequest data: {}\nErrors: {}'.format(
            'Invalid' if self.errors else 'Valid',
            dict(self.request_dict),                        # type-casting to dict for correct string representation
            dict(self.errors) if self.errors else 'None')

    # Allows `if error_report.has_errors: ...`
    @property
    def has_errors(self):
        return bool(self.errors)


def get_errors_in_request(request_dict, *, must_have_fields=None, **kwargs):
    """
    Returns an error report if the request_dict is invalid.
    All named arguments must be passed as named arguments only. Sequential arguments are not allowed
    after `request_dict`.

    :param request_dict: Parsed request data from Sendgrid
    :type request_dict: dict
    :param must_have_fields: List of fields which must be present in a valid request_dict
    :type must_have_fields: list
    :return: Error report (contains a dict of errors found with their details)
    :rtype: RequestErrorReport
    """
    error_report = RequestErrorReport(request_dict)

    # Check if request dict has any of the must have fields missing
    if must_have_fields is not None:
        missing = [key for key in must_have_fields if key not in request_dict]
        if missing:
            error_report.errors['missing_arguments'] = missing

    return error_report
