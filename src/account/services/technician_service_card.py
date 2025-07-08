from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.media.selectors import get_upload_service_card_media
from src.parametric.models import Brand
from src.account.models import TechnicianServiceCard
from src.authentication.selectors.auth import get_user


def create_technician_service_card(
        *,
        technician_id: str,
        brand: str,
        photo: str,
) -> TechnicianServiceCard:

        # Fetch the technician and device type from the database
        technician = get_user(id=technician_id)
        if not technician.groups.filter(name='TECHNICIAN').exists(): raise CustomAPIException(_("Skills can only be assigned to technician users."))

        brand_instance = Brand.objects.get(title__iexact=brand)

        # Create the TechnicianServiceCard instance
        technician_service_card = TechnicianServiceCard.objects.create(
            user=technician,
            brand=brand_instance,
            photo=get_upload_service_card_media(photo),
        )

        return technician_service_card


def update_technician_service_card(
        *,
        instance: TechnicianServiceCard,
        brand: str | None = None,
        photo: str | None = None,
) -> TechnicianServiceCard:
        print(brand)
        if brand:
            brand_instance = Brand.objects.get(title__iexact=brand)
            instance.brand = brand_instance

        if photo:
            instance.photo = get_upload_service_card_media(photo)

        instance.save()
        return instance


def delete_technician_service_card(
        *,
        instance: TechnicianServiceCard,
):
    try:
        instance.delete()

    except Exception as e:
        raise Exception(_("Error delete technician service card."))
