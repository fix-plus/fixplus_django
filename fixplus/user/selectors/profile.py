from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from fixplus.user.models import BaseUser
from fixplus.user.models.profile import Profile, LandLineNumber, MobileNumber


def get_profile(user: BaseUser) -> Profile:
    try:
        return Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        raise Exception(_("Profile does not exist"))


def get_land_line_numbers(user: BaseUser) -> LandLineNumber:
    return LandLineNumber.objects.filter(user=user)


def get_mobile_numbers(user: BaseUser) -> MobileNumber:
    return MobileNumber.objects.filter(user=user)
