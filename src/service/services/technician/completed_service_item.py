from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException
from src.service.models import Service
from src.service.selectors.service import get_service


def add_completed_service_item(
    *,
    service:  Service,
    description: str,
    cost: int,
    quantity: int = 1,
    **kwargs,
):
    from src.service.models import CompletedServiceItem

    with transaction.atomic():
        completed_item = CompletedServiceItem(
            service=service,
            description=description,
            cost=cost,
            quantity=quantity,
        )
        completed_item.full_clean()
        completed_item.save()
