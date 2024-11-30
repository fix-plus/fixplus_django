from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from fixplus.user.models import BaseUser


# Cache ----------------------------------------------------------------------------------------------------------------
def get_cache_verification_mobile_otp(mobile: str) -> bool|None:
    cache_key = mobile + "_verification_mobile_otp"
    cache_value = cache.get(cache_key)
    return cache_value


# Db -------------------------------------------------------------------------------------------------------------------
def get_user(id: str = None, mobile: str=None) -> BaseUser:

    if mobile is not None: return BaseUser.objects.get(mobile=mobile)
    if id is not None: return BaseUser.objects.get(id=id)
    else: raise Exception("User not found.")


def is_exist_user(
        mobile:str = None,
        id: str = None
) -> bool:
    if mobile is not None: return BaseUser.objects.filter(mobile=mobile).exists()
    if id is not None: return BaseUser.objects.filter(id=id).exists()
    else:
        raise Exception


def is_verified_mobile(mobile: str = None,) -> bool:
    if BaseUser.objects.filter(mobile=mobile, is_verified_mobile=True).exists(): return True
    return False


def get_tokens_user(*, mobile:str=None, user:BaseUser=None) -> dict:
    global db_user

    if mobile: db_user = BaseUser.objects.filter(mobile=mobile)
    if user:db_user = user
    if not user and not db_user.exists(): raise Exception("User not found.")

    db_user = db_user.first() if user is None else db_user
    if mobile and not is_verified_mobile(mobile=mobile): raise Exception("User not verified, please verified mobile first.")
    if user and not user.is_verified_mobile: raise Exception( "User not verified, please verified mobile first.")

    return {
        "tokens": db_user.get_tokens(),
        "is_verified_mobile": db_user.is_verified_mobile,
        "is_admin": db_user.is_admin,
        "is_staff": db_user.is_staff,
        "is_technician": db_user.is_technician,
        "status": db_user.status,
    }