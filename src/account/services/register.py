from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException


def update_register(user: User):
    if user.status == 'registered': raise CustomAPIException(_("You have already registered."))
    if user.status == 'rejected': raise CustomAPIException(_("Your request has already been rejected by the admin."))
    if user.status == 'checking': raise CustomAPIException(_("Your request has already been submitted. Please refrain from resubmitting it."))

    fields_to_check = [
        (_('full_name'), user.profile.full_name),
        (_('national_code'), user.profile.national_code),
        (_('gender'), user.profile.gender),
        (_('address'), user.profile.address),
        (_('avatar'), user.profile.avatar),
        (_('identify_document_photo'), user.profile.identify_document_photo),
    ]

    for field_name, field_value in fields_to_check:
        if field_value is None or (isinstance(field_value, str) and field_value.strip() == ''):
            raise CustomAPIException(field_name + _(" cannot be None or empty."))

    user.status = 'checking'
    user.request_register_datetime = timezone.now()
    user.save()