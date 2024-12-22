from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fixplus.user.models import Profile, BaseUser
from fixplus.user.services.group import assign_groups_to_user


def update_register(user: BaseUser):
    if user.status == 'registered': raise Exception(_("You have already registered."))
    if user.status == 'rejected': raise Exception(_("Your request has already been rejected by the admin."))
    if user.status == 'checking': raise Exception(_("Your request has already been submitted. Please refrain from resubmitting it."))

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
            raise Exception(field_name + _(" cannot be None or empty."))

    user.status = 'checking'
    user.request_register_datetime = timezone.now()
    user.save()