from src.parametric.models import Brand
from src.account.models import TechnicianSkill
from src.account.selectors.user import get_user


def search_technician_skill(
        *,
        technician_id:  str | None = None,
        device_type: str | None = None,
        brand_names:list | None = None,
        sort_by: str = 'created_at',
        order: str = 'desc'  # Default to descending order
):

    queryset = TechnicianSkill.objects.all()

    if technician_id:
        queryset = queryset.filter(technician=get_user(id=technician_id))

    if device_type:
        queryset = queryset.filter(device_type=device_type)

    if brand_names:
        instance_brand_names = Brand.objects.filter(title__in=brand_names)
        queryset = queryset.filter(brand_names__in=instance_brand_names)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at', ]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'updated_at',.")

    return queryset


def get_technician_skill(
        *,
        id: str
):
    return TechnicianSkill.objects.get(id=id)