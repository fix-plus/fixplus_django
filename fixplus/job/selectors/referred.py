from django.db.models import QuerySet

from fixplus.job.models import ReferredJob
from fixplus.user.selectors.user import get_user


def get_referred_job(*, id:str) -> ReferredJob:
    return ReferredJob.objects.get(id=id)


def search_referred_job_list(
    technician_id: str | None = None,
    referred_by_id: str | None = None,
    updated_by_id: str | None = None,
    customer_name: str = None,
    customer_phone_number: str = None,
    device_type: str = None,
    brand_name: str = None,
    status: str | None = None,
    address: str = None,
    sort_by: str = None,
    order: str = 'desc'  # Default to descending order
) -> QuerySet:
    # Start with the Job queryset
    queryset = ReferredJob.objects.all()

    # Filter by technician_id if provided
    if technician_id:
        queryset = queryset.filter(technician=get_user(id=technician_id))

    # Filter by referred_by_id if provided
    if referred_by_id:
        queryset = queryset.filter(referred_by=get_user(id=referred_by_id))

    # Filter by updated_by_id if provided
    if updated_by_id:
        queryset = queryset.filter(updated_by=get_user(id=updated_by_id))

    # Filter by customer_name if provided
    if customer_name:
        queryset = queryset.filter(job__customer__full_name__istartswith=customer_name)

    # Filter by customer_mobile if provided
    if customer_phone_number:
        queryset = queryset.filter(job__customer__customerphonenumber__number__startswith=customer_phone_number)

    # Filter by device_type if provided
    if device_type:
        queryset = queryset.filter(job__device_type__iexact=device_type)

    # Filter by brand_name if provided
    if brand_name:
        queryset = queryset.filter(job__brand_name__iexact=brand_name)

    # Filter by status if provided
    if status:
        status = status.split(',')
        queryset = queryset.filter(status__in=status)

    # Filter by address if provided
    if address:
        queryset = queryset.filter(job__address__icontains=address)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at']:  # Add any other fields you want to sort by
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'updated_at'.")

    return queryset