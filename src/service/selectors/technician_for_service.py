from django.db.models import Q, Count
from geopy.distance import geodesic

from src.account.models import UserRegistryRequest, TechnicianStatus
from src.service.models import Service
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
        groups__name='TECHNICIAN'
    ).annotate(
        group_count=Count('groups')
    ).filter(
        Q(registry_requests__status=UserRegistryRequest.Status.APPROVED) &
        Q(technician_statuses__status=TechnicianStatus.Status.ACTIVE)
    ).distinct()

    # Set filter of brand and device type
    service_location = None
    if service_id:
        db_service = Service.objects.filter(id=service_id).first()

        if not db_service:
            return queryset.none()

        queryset = queryset.filter(
            Q(technician_skills__device_type=db_service.device_type) &
            Q(technician_skills__brand_names=db_service.brand)
        )

        # Store service location for distance calculation
        if db_service.address and db_service.address.latitude and db_service.address.longitude:
            service_location = (db_service.address.latitude, db_service.address.longitude)

    # Filter by mobile if provided
    if mobile:
        queryset = queryset.filter(mobile__startswith=mobile)

    # Join with Profile to filter by full_name if provided
    if full_name:
        queryset = queryset.filter(profile__full_name__istartswith=full_name)

    # Evaluate the queryset once
    technicians = list(queryset.all())

    # Calculate distances for all technicians if service_location exists
    if service_location:
        for technician in technicians:
            try:
                user_latest_location = technician.location_trackers.latest('created_at')
                if user_latest_location and user_latest_location.latitude and user_latest_location.longitude:
                    user_location = (user_latest_location.latitude, user_latest_location.longitude)
                    technician.distance = round(geodesic(service_location, user_location).km, 1)
                else:
                    technician.distance = None
            except:
                technician.distance = None
    else:
        # If no service location, set distance to None for all technicians
        for technician in technicians:
            technician.distance = None

    # Handle sorting
    order_prefix = '-' if order == 'desc' else ''
    if sort_by:
        if sort_by in ['created_at', 'last_online']:
            # Re-query with proper ordering for database fields
            return queryset.order_by(f"{order_prefix}{sort_by}")
        elif sort_by == 'distance':
            if not service_location:
                raise ValueError("Cannot sort by distance without a valid service address.")
            # Sort by distance in-memory, handling None values
            technicians = sorted(
                technicians,
                key=lambda x: x.distance if x.distance is not None else float('inf'),
                reverse=(order == 'desc')
            )
            return technicians
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online', 'distance'.")

    return technicians