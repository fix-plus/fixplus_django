from src.parametric.models import Brand
from src.account.models import TechnicianServiceCard
from src.authentication.selectors.auth import get_user


def search_technician_service_card(
        *,
        technician_id:  str | None = None,
        brands:list | None = None,
        sort_by: str = 'created_at',
        order: str = 'desc'  # Default to descending order
):

    queryset = TechnicianServiceCard.objects.all()
    if technician_id:
        queryset = queryset.filter(user=get_user(id=technician_id))

    if brands:
        instance_brands = Brand.objects.filter(title__in=brands)
        queryset = queryset.filter(brand__in=instance_brands)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at', ]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'updated_at',.")

    return queryset


def get_technician_service_card(
        *,
        id: str
):
    return TechnicianServiceCard.objects.get(id=id)