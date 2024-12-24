from django.db.models import Q, Count, QuerySet

from fixplus.job.models import Job, ReferredJob


def search_job_list(
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
    queryset = Job.objects.all()

    # Filter by customer_name if provided
    if customer_name:
        queryset = queryset.filter(customer__full_name__istartswith=customer_name)

    # Filter by customer_mobile if provided
    if customer_phone_number:
        queryset = queryset.filter(customer__customerphonenumber__number__startswith=customer_phone_number)

    # Filter by device_type if provided
    if device_type:
        queryset = queryset.filter(device_type__iexact=device_type)

    # Filter by brand_name if provided
    if brand_name:
        queryset = queryset.filter(brand_name__iexact=brand_name)

    # Filter by status if provided
    if status:
        status = status.split(',')
        queryset = queryset.filter(status__in=status)

    # Filter by address if provided
    if address:
        queryset = queryset.filter(address__icontains=address)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at']:  # Add any other fields you want to sort by
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'updated_at'.")

    return queryset


def get_job(*, id:str) -> Job:
    return  Job.objects.get(id=id)


def get_assigned_job(*, id:str) -> ReferredJob:
    return ReferredJob.objects.get(id=id)