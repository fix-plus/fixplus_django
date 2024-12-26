from django.db.models import Q, Count

from fixplus.job.selectors.job import get_job
from fixplus.user.models import BaseUser


def search_technician_for_job(
        job_id: str = None,
        mobile: str = None,
        full_name: str | None = None,
        sort_by: str = 'last_online',
        order: str = 'desc'  # Default to descending order
) -> BaseUser:
    queryset = BaseUser.objects.filter(groups__name='technician').annotate(group_count=Count('groups')).distinct()

    if job_id:
        db_job = get_job(id=job_id)

        if not db_job:
            return queryset.none()

        queryset = queryset.filter(
            technician_skill_technician__device_type=db_job.device_type,
            technician_skill_technician__brand_names=db_job.brand_name
        )

    # General filter
    queryset = queryset.filter(status='registered', profile__is_in_holiday=False)

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
        if sort_by in ['created_at', 'last_online', ]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online'.")

    return queryset
