from django.db.models import Q

from src.account.services.technician_status import get_active_technicians
from src.service.models import Service


def get_admin_dashboard_metric():
    awaiting_services_count = Service.objects.filter(status=Service.Status.WAITING).count()
    available_technicians_count = get_active_technicians().count()
    processing_services_count = Service.objects.filter(
        Q(status=Service.Status.ACCEPTED) |
        Q(status=Service.Status.REFERRED_TO_SHOP)
    )
    withdrawal_requests_count = 1

    return {
        "awaiting_services_count": awaiting_services_count,
        "available_technicians_count": available_technicians_count,
        "processing_services_count": processing_services_count.count(),
        "withdrawal_requests_count": withdrawal_requests_count
    }