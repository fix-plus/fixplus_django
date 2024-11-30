from django.core.exceptions import ObjectDoesNotExist

from fixplus.user.models import Profile, BaseUser
from fixplus.user.models.profile import LandLineNumber, MobileNumber


def create_profile(*args, **kwargs):
    return Profile.objects.create(*args, **kwargs)


def create_land_line_numbers(*, user: BaseUser, number:str):
    return LandLineNumber.objects.create(
        user=user,
        number=number
    )


def create_mobile_numbers(*, user: BaseUser, number:str):
    return MobileNumber.objects.create(
        user=user,
        number=number
    )


def update_profile(instance: Profile, *args, **kwargs):
    for key, value in kwargs.items():
        if key == 'land_line_numbers' and value is not None:
            for number in value:
                create_land_line_numbers(user=instance.user, number=number)
        if key == 'mobile_numbers' and value is not None:
            for number in value:
                create_mobile_numbers(user=instance.user, number=number)
        elif value is not None:
            setattr(instance, key, value)
    instance.save()

    return instance