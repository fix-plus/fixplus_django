from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ValidationError as drf_ValidationError,
    NotFound as drf_NotFound,
    ParseError,
    MethodNotAllowed,
    PermissionDenied as drf_PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
    UnsupportedMediaType,
    Throttled,
    NotAcceptable,
)
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    SuspiciousOperation,
    FieldError,
    ValidationError as django_ValidationError,
    PermissionDenied as django_PermissionDenied,
    AppRegistryNotReady,
    EmptyResultSet,
    FullResultSet,
    FieldDoesNotExist,
    ImproperlyConfigured,
    ViewDoesNotExist,
    MiddlewareNotUsed,
    DisallowedRedirect,
    DisallowedHost,
    RequestAborted,
    RequestDataTooBig,
    SynchronousOnlyOperation,
    SuspiciousMultipartForm,
    SuspiciousFileOperation,
    TooManyFieldsSent,
    TooManyFilesSent, BadRequest,
)
import logging

from src.common.custom_exception import CustomAPIException

logger = logging.getLogger(__name__)

def clean_error_message(message):
    """Utility function to clean up error messages."""
    return message.replace('\n', ' ').replace('"', '').strip()

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django Rest Framework.

    This function formats all error responses to ensure they have a consistent structure.
    The response will always include a 'status', 'message', and 'errors' key, where 'errors'
    is a list of strings.

    Args:
        exc: The exception raised.
        context: The context in which the exception was raised.

    Returns:
        A standardized error response.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Initialize a default response structure
    response_data = {
        "status": "error",
        "message": _("An unexpected error occurred."),
        "errors": []
    }

    if response is None:
        # If the response is None, it means the exception is not handled by DRF
        response_data["errors"].append(clean_error_message(str(exc)))
        return Response(response_data, status=500)

    # Customize the response for DRF handled exceptions
    if isinstance(exc, CustomAPIException):
        response_data["message"] = str(exc.detail)
        response_data["errors"] = exc.errors
    elif isinstance(exc, drf_ValidationError):
        response_data["message"] = _("Validation failed.")
        response_data["errors"] = []
        if isinstance(exc.detail, list):
            response_data["errors"].extend([clean_error_message(err) for err in exc.detail])
        elif isinstance(exc.detail, dict):
            for field, messages in exc.detail.items():
                for message in messages:
                    response_data["errors"].append(clean_error_message(f"'{field}' {message}"))
    elif isinstance(exc, drf_NotFound) or isinstance(exc, Http404):
        response_data["message"] = _("The requested resource was not found.")
        response_data["errors"].append(_("Not found."))
    elif isinstance(exc, ParseError):
        response_data["message"] = _("Malformed request.")
        response_data["errors"].append(_("The request could not be parsed."))
    elif isinstance(exc, MethodNotAllowed):
        response_data["message"] = _("Method not allowed.")
        response_data["errors"].append(_("This method is not allowed for the requested URL."))
    elif isinstance(exc, drf_PermissionDenied) or isinstance(exc, django_PermissionDenied):
        response_data["message"] = _("Permission denied.")
        response_data["errors"].append(_("You do not have permission to perform this action."))
    elif isinstance(exc, AuthenticationFailed):
        response_data["message"] = _("Authentication failed.")
        response_data["errors"].append(_("Invalid credentials provided."))
    elif isinstance(exc, NotAuthenticated):
        response_data["message"] = _("Not authenticated.")
        response_data["errors"].append(_("You must be logged in to perform this action."))
    elif isinstance(exc, UnsupportedMediaType):
        response_data["message"] = _("Unsupported media type.")
        response_data["errors"].append(_("The media type of the request is not supported."))
    elif isinstance(exc, Throttled):
        response_data["message"] = _("Request limit exceeded.")
        response_data["errors"].append(_("You have exceeded your request limit."))
    elif isinstance(exc, NotAcceptable):
        response_data["message"] = _("Not acceptable.")
        response_data["errors"].append(_("The requested format is not acceptable."))
    elif isinstance(exc, ObjectDoesNotExist):
        response_data["message"] = _("The requested object does not exist.")
        response_data["errors"].append(_("Object not found."))
    elif isinstance(exc, MultipleObjectsReturned):
        response_data["message"] = _("Multiple objects returned.")
        response_data["errors"].append(_("More than one object was found."))
    elif isinstance(exc, SuspiciousOperation):
        response_data["message"] = _("Suspicious operation detected.")
        response_data["errors"].append(_("A suspicious operation was attempted."))
    elif isinstance(exc, FieldError):
        response_data["message"] = _("Field error.")
        response_data["errors"].append(_("There was an error with a field."))
    elif isinstance(exc, django_ValidationError):
        response_data["message"] = _("Validation failed.")
        response_data["errors"] = []
        if isinstance(exc.message_dict, dict):
            for field, messages in exc.message_dict.items():
                for message in messages:
                    response_data["errors"].append(clean_error_message(f"{message} ({field})"))
        else:
            response_data["errors"].append(clean_error_message(str(exc)))
    elif isinstance(exc, AppRegistryNotReady):
        response_data["message"] = _("App registry is not ready.")
        response_data["errors"].append(_("The application registry is not ready."))
    elif isinstance(exc, EmptyResultSet):
        response_data["message"] = _("Empty result set.")
        response_data["errors"].append(_("No results were found."))
    elif isinstance(exc, FullResultSet):
        response_data["message"] = _("Full result set.")
        response_data["errors"].append(_("The result set is full."))
    elif isinstance(exc, FieldDoesNotExist):
        response_data["message"] = _("Field does not exist.")
        response_data["errors"].append(_("The specified field does not exist."))
    elif isinstance(exc, ImproperlyConfigured):
        response_data["message"] = _("Improperly configured.")
        response_data["errors"].append(_("The application is improperly configured."))
    elif isinstance(exc, ViewDoesNotExist):
        response_data["message"] = _("View does not exist.")
        response_data["errors"].append(_("The specified view does not exist."))
    elif isinstance(exc, MiddlewareNotUsed):
        response_data["message"] = _("Middleware not used.")
        response_data["errors"].append(_("The specified middleware is not used."))
    elif isinstance(exc, TooManyFilesSent):
        response_data["message"] = _("Too many files sent.")
        response_data["errors"].append(_("You have sent too many files."))
    elif isinstance(exc, TooManyFieldsSent):
        response_data["message"] = _("Too many fields sent.")
        response_data["errors"].append(_("You have sent too many fields."))
    elif isinstance(exc, SuspiciousFileOperation):
        response_data["message"] = _("Suspicious file operation.")
        response_data["errors"].append(_("A suspicious file operation was attempted."))
    elif isinstance(exc, SuspiciousMultipartForm):
        response_data["message"] = _("Suspicious multipart form.")
        response_data["errors"].append(_("A suspicious multipart form was submitted."))
    elif isinstance(exc, SynchronousOnlyOperation):
        response_data["message"] = _("Synchronous operation not allowed.")
        response_data["errors"].append(_("This operation cannot be performed synchronously."))
    elif isinstance(exc, RequestDataTooBig):
        response_data["message"] = _("Request data too big.")
        response_data["errors"].append(_("The request data is too large."))
    elif isinstance(exc, BadRequest):
        response_data["message"] = _("Bad request.")
        response_data["errors"].append(_("The request was malformed or invalid."))
    elif isinstance(exc, RequestAborted):
        response_data["message"] = _("Request aborted.")
        response_data["errors"].append(_("The request was aborted."))
    elif isinstance(exc, DisallowedHost):
        response_data["message"] = _("Disallowed host.")
        response_data["errors"].append(_("The host is not allowed."))
    elif isinstance(exc, DisallowedRedirect):
        response_data["message"] = _("Disallowed redirect.")
        response_data["errors"].append(_("The redirect is not allowed."))

    return Response(response_data, status=response.status_code) if response else Response(response_data, status=500)