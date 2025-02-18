from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.parametric.models import DeviceType, Brand
from src.account.models import TechnicianSkill
from src.authentication.selectors.auth import get_user


def create_technician_skill(
        *,
        technician_id: str,
        device_type: str,
        brand_names: list,
) -> TechnicianSkill:
    try:
        # Fetch the technician and device type from the database
        technician = get_user(id=technician_id)
        if not technician.groups.filter(name='technician').exists(): raise CustomAPIException(_("Skills can only be assigned to technician users."))

        device_type_instance = DeviceType.objects.get(title__iexact=device_type)

        # Create the TechnicianSkill instance
        technician_skill = TechnicianSkill.objects.create(
            user=technician,
            device_type=device_type_instance
        )

        # Add brand names to the ManyToMany field
        if brand_names:
            brands = Brand.objects.filter(title__in=brand_names)
            technician_skill.brand_names.set(brands)

        return technician_skill

    except Exception as e:
        # Handle the case where the technician or device type does not exist
        raise CustomAPIException(_("Error creating technician skill."))


def update_technician_skill(
        *,
        instance: TechnicianSkill,
        device_type: str | None = None,
        brand_names: list | None = None,
) -> TechnicianSkill:
    try:
        if device_type:
            device_type_instance = DeviceType.objects.get(title__iexact=device_type)
            instance.device_type = device_type_instance
        if brand_names:
            brands = Brand.objects.filter(title__in=brand_names)
            instance.brand_names.clear()
            instance.brand_names.set(brands)

        instance.save()
        return instance

    except Exception as e:
        # Handle the case where the technician or device type does not exist
        raise CustomAPIException(_("Error update technician skill."))


def delete_technician_skill(
        *,
        instance: TechnicianSkill,
):
    try:
        instance.delete()

    except Exception as e:
        # Handle the case where the technician or device type does not exist
        raise Exception(_("Error delete technician skill."))
