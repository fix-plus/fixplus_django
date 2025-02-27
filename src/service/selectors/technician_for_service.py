from django.db.models import Q, Count, When, Case, F, Value, FloatField
from django.db.models.functions import Cast
from geopy.distance import geodesic

from src.account.models import UserRegistryRequest, TechnicianStatus
from src.service.selectors.service import get_service
from src.authentication.models import User


def search_technician_for_service(
        service_id: str = None,
        mobile: str = None,
        full_name: str | None = None,
        sort_by: str = 'last_online',
        order: str = 'desc'  # Default to descending order
) -> User:
    # Initial queryset
    queryset = User.objects.filter(
        groups__name='technician'
    ).annotate(
        group_count=Count('groups')
    ).filter(
        Q(registry_requests__status=UserRegistryRequest.APPROVED) &
        Q(technician_statuses__status=TechnicianStatus.ACTIVE)
    ).distinct()

    # Set filter of brand and device type
    if service_id:
        db_service = get_service(id=service_id)

        if not db_service:
            return queryset.none()

        queryset = queryset.filter(
            Q(technician_skills__device_type=db_service.device_type) &
            Q(technician_skills__brand_names=db_service.brand)
        )

        # Calculate distance
        service_address = db_service.address
        if service_address and service_address.latitude and service_address.longitude:
            service_location = (service_address.latitude, service_address.longitude)

            # Annotate distance using a subquery
            queryset = queryset.annotate(
                distance=Case(
                    When(
                        Q(addresses__latitude__isnull=False) &
                        Q(addresses__longitude__isnull=False),
                        then=Value(None)  # Placeholder for distance calculation
                    ),
                    default=None,
                    output_field=FloatField()
                )
            )

            # Calculate the distance in Python after fetching the queryset
            queryset = list(queryset)  # Evaluate the queryset to get the results
            for user in queryset:
                user_address = user.addresses.latest('created_at')
                if user_address and user_address.latitude and user_address.longitude:
                    user_location = (user_address.latitude, user_address.longitude)
                    user.distance = round(geodesic(service_location, user_location).km, 1)

                else:
                    user.distance = None

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