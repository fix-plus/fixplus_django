from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class CustomAPIException(APIException):
    status_code = 400
    default_message = _('An error occurred.')

    def __init__(self, message=None, errors=None, status_code=None):
        # Set the message
        self.detail = message if message is not None else self.default_message

        # Set the errors
        self.errors = errors if errors is not None else [self.detail]

        # Set the status code
        if status_code is not None:
            self.status_code = status_code