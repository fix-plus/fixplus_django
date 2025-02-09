import random
import string
from django.core import signing
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from src.account.selectors.user import get_cache_verification_mobile_otp


def generate_otp_code():
    return str(random.randint(1000, 9999))


def generate_referral_code(*, length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits
    referral_code = ''.join(random.choice(characters) for _ in range(length))
    return str(referral_code)


def generate_one_time_token(email):
    """
    Create a signed token using the provided email.
    """
    try:
        token_data = {'email': email}
        token = signing.dumps(token_data, key=settings.SECRET_KEY)
        return token
    except Exception as e:
        # Handle exceptions accordingly
        raise e


def verify_otp(*, mobile, code):
    cache_otp_code = get_cache_verification_mobile_otp(mobile=mobile)
    if not cache_otp_code or str(cache_otp_code) != str(code):
        raise Exception(_("Verification code is expired or invalid."))
    return True
