from django.core.exceptions import ObjectDoesNotExist

from fixplus.upload.selectors import get_upload_identify_document_media
from fixplus.user.models import Profile, BaseUser
from fixplus.user.models.profile import LandLineNumber, MobileNumber


def create_profile(*args, **kwargs):
    return Profile.objects.create(*args, **kwargs)


def create_land_line_numbers(*, user: BaseUser, number: str):
    return LandLineNumber.objects.get_or_create(
        user=user,
        number=number
    )


def create_mobile_numbers(*, user: BaseUser, number: str):
    return MobileNumber.objects.get_or_create(
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
        if key == 'identify_document_photo_id' and value is not None:
            instance.identify_document_photo = get_upload_identify_document_media(id=value)
        if key == 'other_identify_document_photos_id' and value is not None:
            instance.other_identify_document_photos.clear()
            for media_id in value:
                instance.other_identify_document_photos.add(get_upload_identify_document_media(id=media_id))
        elif value is not None:
            setattr(instance, key, value)
    instance.save()

    return instance
