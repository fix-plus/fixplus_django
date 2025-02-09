from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from src.account.models import Profile
from src.common.custom_exception import CustomAPIException
from src.authentication.models import User


def get_profile(user: User) -> Profile:
    try:
        return Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        raise CustomAPIException(_("Profile does not exist"))
