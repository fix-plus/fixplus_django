from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.account.models import UserRegistryRequest
from src.authentication.models import User
from src.common.custom_exception import CustomAPIException


def update_register(user: User):
    # Init
    db_registry_req = UserRegistryRequest.objects.filter(user=user)

    # Validator
    if not db_registry_req.exists(): raise CustomAPIException(_("Identify document cannot be None or empty."))
    if db_registry_req.filter(status='approved').exists(): raise CustomAPIException(_("You are already verified. There is no need to reapply."))
    if db_registry_req.latest('created_at').status == 'checking': raise CustomAPIException(_("Your request has already been submitted. Please refrain from resubmitting it."))
    if db_registry_req.latest('created_at').status != 'draft': raise CustomAPIException(_("Identify document cannot be None or empty."))

    fields_to_check = [
        (_('full_name'), user.profile.full_name),
        (_('national_code'), user.profile.national_code),
        (_('gender'), user.profile.gender),
        (_('address'), user.profile.address),
        (_('avatar'), user.profile.avatar),
    ]

    for field_name, field_value in fields_to_check:
        if field_value is None or (isinstance(field_value, str) and field_value.strip() == ''):
            raise CustomAPIException(field_name + _(" cannot be None or empty."))

    db_registry_req = db_registry_req.latest('created_at')

    db_registry_req.status = 'checking'
    db_registry_req.updated_at = timezone.now()
    db_registry_req.save()