from fixplus.user.models import TechnicianSkill
from fixplus.user.selectors.user import get_user


def search_technician_skill(
        *,
        technician_id: str,
        device_type: str | None = None,
):
    queryset = TechnicianSkill.objects.filter(technician=get_user(id=technician_id))

    if device_type:
        queryset = queryset.filter(device_type=device_type)

    return queryset.order_by('-created_at')


def get_technician_skill(
        *,
        id: str
):
    return TechnicianSkill.objects.get(id=id)