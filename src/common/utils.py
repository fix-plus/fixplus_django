from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured
from jdatetime import datetime as jdatetime
from django.utils import timezone

from rest_framework import serializers


def make_mock_object(**kwargs):
    return type("", (object, ), kwargs)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(f"{error_message_prefix} Could not find: {stringified_not_present}")

    return values


def check_all_int(input_str):
    """
    Check if all characters in a string are integers.

    Args:
    input_str (str): The input string to check.

    Returns:
    bool: True if all characters are integers, False otherwise.
    """
    for char in input_str:
        if not char.isdigit():
            return False
    return True


def to_jalali_date_string(gregorian_date, format_string='%Y/%m/%d'):
    """
    تبدیل تاریخ میلادی به شمسی با رعایت تایم‌زون
    :param gregorian_date: تاریخ میلادی (datetime یا date)
    :param format_string: فرمت خروجی رشته (مثل '1404/07/08')
    :return: رشته تاریخ شمسی
    """
    if not gregorian_date:
        return ''
    local_date = timezone.localtime(gregorian_date) if hasattr(gregorian_date, 'tzinfo') else gregorian_date
    jalali_date = jdatetime.fromgregorian(
        year=local_date.year,
        month=local_date.month,
        day=local_date.day
    )
    return jalali_date.strftime(format_string)
