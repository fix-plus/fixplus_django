from django.utils.translation import gettext_lazy as _


from src.common.custom_exception import CustomAPIException
from src.account.models import TechnicianServiceZone
from src.authentication.selectors.auth import get_user


def create_technician_service_zone(
        *,
        technician_id: str,
        zone: str,
) -> TechnicianServiceZone:

        # Fetch the technician and device type from the database
        technician = get_user(id=technician_id)
        if not technician.groups.filter(name='TECHNICIAN').exists(): raise CustomAPIException(_("Service zone can only be assigned to technician users."))

        # Create the TechnicianServiceZone instance
        technician_service_zone = TechnicianServiceZone.objects.create(
            user=technician,
            zone=zone,
        )

        return technician_service_zone




def update_technician_service_zone(
        *,
        instance: TechnicianServiceZone,
        zone: str | None = None,
) -> TechnicianServiceZone:

        if zone:
            instance.zone = zone

        instance.save()
        return instance


def delete_technician_service_zone(
        *,
        instance: TechnicianServiceZone,
):
    try:
        instance.delete()

    except Exception as e:
        raise Exception(_("Error delete technician service zone."))
