from django.db.models import Subquery
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.customer.models import Customer, CustomerContactNumber


def search_customer_list(
    phone: str = None,
    full_name: str | None = None,
    sort_by: str = 'created_at',
    order: str = 'desc'  # Default to descending order
) -> Customer :

    queryset = Customer.objects.all()

    # Filter by mobile if provided
    if phone:
        mobile_queryset = CustomerContactNumber.objects.filter(number__startswith=phone)
        customer_ids = mobile_queryset.values_list('customer_id', flat=True).distinct()
        queryset = Customer.objects.filter(id__in=customer_ids)
        queryset = queryset.annotate(
            searched_phone_number=Subquery(mobile_queryset.values('number')[:1])
        )

    # Join with Profile to filter by full_name if provided
    if full_name:
        queryset = queryset.filter(full_name__istartswith=full_name)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at',]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online',.")

    return queryset


def get_customer(*, id: str) -> Customer:
    try:
        return Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        raise CustomAPIException(_("Customer doesn't exist."), status.HTTP_404_NOT_FOUND)