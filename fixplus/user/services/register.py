from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from fixplus.user.models import Profile, BaseUser
from fixplus.user.services.group import assign_groups_to_user


def update_register(user: BaseUser):
    if user.groups.all().exists(): raise Exception(_("You don't need to register."))
    if user.status == 'registered': raise Exception(_("You have already registered."))
    # if user.profile.avatar is None: raise Exception(_("Uploading an avatar photo is required."))
    # if user.profile.identify_document_photo is None: raise Exception(_("Uploading a picture of your national ID card or passport is required."))
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

    assign_groups_to_user(user=user, group_names=['technician'])
    user.status = 'checking'
    user.save()