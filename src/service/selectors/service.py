from django.db.models import Q, Count, QuerySet

from src.service.models import Service


def search_service_list(
    customer_name: str = None,
    customer_phone_number: str = None,
    device_type: str = None,
    brand: str = None,
    status: str | None = None,
    address: str = None,
    sort_by: str = None,
    order: str = 'desc'  # Default to descending order
) -> QuerySet:
    # Start with the Service queryset
    queryset = Service.objects.all()

    # Filter by customer_name if provided
    if customer_name:
        queryset = queryset.filter(customer__full_name__istartswith=customer_name)

    # Filter by customer_mobile if provided
    if customer_phone_number:
        queryset = queryset.filter(customer__contact_numbers__number__startswith=customer_phone_number)

    # Filter by device_type if provided
    if device_type:
        queryset = queryset.filter(device_type__title__iexact=device_type)

    # Filter by brand_name if provided
    if brand:
        queryset = queryset.filter(brand__title__iexact=brand)

    # Filter by status if provided
    if status:
        status = status.split(',')
        queryset = queryset.filter(status__in=status)

    # Filter by address if provided
    if address:
        queryset = queryset.filter(address__address__icontains=address)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at']:  # Add any other fields you want to sort by
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'updated_at'.")

    return queryset


def get_service(*, id:str) -> Service:
    return  Service.objects.get(id=id)