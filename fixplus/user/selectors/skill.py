from fixplus.parametric.models import BrandNameParametric
from fixplus.user.models import TechnicianSkill
from fixplus.user.selectors.user import get_user


def search_technician_skill(
        *,
        technician_id:  str | None = None,
        device_type: str | None = None,
        brand_names:list | None = None,
):

    queryset = TechnicianSkill.objects.all()

    if technician_id:
        queryset = queryset.filter(technician=get_user(id=technician_id))

    if device_type:
        queryset = queryset.filter(device_type=device_type)

    if brand_names:
        instance_brand_names = BrandNameParametric.objects.filter(title__in=brand_names)
        queryset = queryset.filter(brand_names__in=instance_brand_names)

    return queryset.order_by('-created_at')


def get_technician_skill(
        *,
        id: str
):
    return TechnicianSkill.objects.get(id=id)