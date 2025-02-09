from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.authentication.models import User
from src.account.selectors.user import is_verified_mobile
from src.account.services.group import assign_groups_to_user
from src.account.services.profile import update_profile
from src.account.utils import verify_otp


def create_user(*, mobile:str=None) -> User:
    db_user = User.objects.filter(mobile=mobile)

    if db_user.exists():
        db_user = db_user.first()
        return db_user

    return User.objects.create_user(mobile=mobile)


def update_user(instance: User, *args, **kwargs):
    for key, value in kwargs.items():
        if key == 'group' and value is not None:
            instance.groups.clear()
            assign_groups_to_user(user=instance, group_names=value)
        if key == 'profile' and value is not None:
            update_profile(instance.profile, **value)
        else:
            if value is not None:
                setattr(instance, key, value)
    instance.save()

    return instance


def set_cache_verification_mobile_otp(mobile: str, otp:str):
    cache_key = mobile + "_verification_mobile_otp"
    cache.delete(cache_key)
    cache.set(cache_key, otp, timeout=2*60)


def update_verified(*, mobile:str, code:str) -> User:
    db_user = User.objects.filter(mobile=mobile)

    if not db_user.exists(): raise CustomAPIException("User not found.")
    if mobile and is_verified_mobile(mobile=mobile): raise CustomAPIException(_("User was verified, please login."))

    if verify_otp(mobile=mobile, code=code):
        db_user = db_user.first()
        db_user.is_verified_mobile = True
        db_user.save()
        return db_user