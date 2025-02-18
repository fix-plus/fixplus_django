from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.geo.models import Address
from src.media.selectors import get_upload_identify_document_media
from src.account.models import Profile, UserRegistryRequest, UserContactNumber


def create_profile(*args, **kwargs):
    return Profile.objects.create(*args, **kwargs)


def update_profile(instance: Profile, *args, **kwargs):
    for key, value in kwargs.items():
        if key == 'contact_numbers' and value is not None:
            for item in value:
                UserContactNumber.objects.get_or_create(
                    user=instance.user,
                    number=item['number'],
                    defaults={
                        'phone_type': item['phone_type'],
                        'is_primary': item['is_primary'],
                    }
                )

        elif key == 'identify_document_photo_id' and value is not None:
            db_registry_req = UserRegistryRequest.objects.filter(user=instance.user)

            # Validator
            if db_registry_req.filter(status='approved').exists(): raise CustomAPIException(
                _("You are already verified. There is no need to reapply."))
            if db_registry_req.exists() and db_registry_req.latest('created_at').status == 'checking': raise CustomAPIException(
                _("Your request has already been submitted. Please refrain from resubmitting it."))

            if not db_registry_req.exists() or db_registry_req.latest('created_at').status == 'rejected':
                UserRegistryRequest.objects.create(
                    user=instance.user,
                    status='draft',
                    identify_document_photo = get_upload_identify_document_media(id=value)
                )
            elif db_registry_req.latest('created_at').status == 'draft':
                db_registry_req = db_registry_req.latest('created_at')
                db_registry_req.identify_document_photo = get_upload_identify_document_media(id=value)
                db_registry_req.save()

        elif key == 'other_identify_document_photos_id' and value is not None:
            db_registry_req = UserRegistryRequest.objects.filter(user=instance.user)

            # Validator
            if db_registry_req.filter(status='approved').exists(): raise CustomAPIException(
                _("You are already verified. There is no need to reapply."))
            if db_registry_req.exists() and db_registry_req.latest('created_at').status == 'checking': raise CustomAPIException(
                _("Your request has already been submitted. Please refrain from resubmitting it."))

            if not db_registry_req.exists() or db_registry_req.latest('created_at').status == 'rejected':
                query = UserRegistryRequest.objects.create(
                    user=instance.user,
                    status='draft',
                )
                for media_id in value:
                    query.other_identify_document_photos.add(get_upload_identify_document_media(id=media_id))
                query.save()
            elif db_registry_req.latest('created_at').status == 'draft':
                db_registry_req = db_registry_req.latest('created_at')
                db_registry_req.other_identify_document_photos.clear()
                for media_id in value:
                    db_registry_req.other_identify_document_photos.add(get_upload_identify_document_media(id=media_id))
                db_registry_req.save()

        elif key == 'address' and value is not None:
            query, is_created = Address.objects.get_or_create(
                user=instance.user,
                address=value
            )
            instance.address = query

        elif key == 'latitude' and value is not None:
            if instance.address is None:
                query, is_created = Address.objects.get_or_create(
                    user=instance.user,
                    latitude=value
                )
                instance.address = query
            else:
                query = instance.address
                query.latitude = value
                query.save()

        elif key == 'longitude' and value is not None:
            if instance.address is None:
                query, is_created = Address.objects.get_or_create(
                    user=instance.user,
                    longitude=value
                )
                instance.address = query
            else:
                query = instance.address
                query.longitude = value
                query.save()


        elif value is not None:
            setattr(instance, key, value)
    instance.save()

    return instance
