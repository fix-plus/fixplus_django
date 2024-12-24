from django.db.models import Q, Count

from fixplus.user.models import BaseUser


def search_technician_for_job(
    mobile: str = None,
    full_name: str | None = None,
    sort_by: str = 'last_online',
    order: str = 'desc'  # Default to descending order
) -> BaseUser :
    # Start with the BaseUser  queryset
    queryset = BaseUser.objects.filter(status='registered', profile__is_in_holiday=False)

    # filter Technicians
    queryset = queryset.filter(groups__name='technician').annotate(group_count=Count('groups')).distinct()

    # Filter by mobile if provided
    if mobile:
        queryset = queryset.filter(mobile__startswith=mobile)

    # Join with Profile to filter by full_name if provided
    if full_name:
        queryset = queryset.filter(profile__full_name__istartswith=full_name)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'last_online',]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online'.")

    return queryset