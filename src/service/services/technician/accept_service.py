from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException
from src.service.models import Service
from src.service.selectors.service import get_service


def accept_service(
    *,
    service_id:  str,
    user: User,
    is_accepted: bool,
    estimate_arrival_at = None,
    reject_reason = None,
    **kwargs,
):
    db_service = get_service(id=service_id)

    # Check Technician of this Service is the same as the user
    if db_service.technician != user:
        raise CustomAPIException(_("This service is not assigned to the technician."), status_code=406)

    # Check Service is in correct status
    if db_service.status != Service.Status.ASSIGNED:
        raise CustomAPIException(_("Service is not in the correct status to be accepted."), status_code=400)

    # Check Service deadline accepting not passed
    if db_service.deadline_accepting_at < timezone.now():
        # Update the service status to EXPIRED
        db_service.set_expired(custom_remark=_("Service accepting deadline has passed."))

        raise CustomAPIException(_("Service deadline accepting has passed."), status_code=400)

    # Check if is_accepted is True and estimate_arrival_at is provided
    if is_accepted and not estimate_arrival_at:
        raise CustomAPIException(_("Estimate arrival time is required when accepting the service."), status_code=400)

    # Check estimate_arrival_at is in the future
    if estimate_arrival_at and estimate_arrival_at <= timezone.now():
        raise CustomAPIException(_("Estimate arrival time must be in the future."), status_code=400)

    # Update the service status and details
    db_service.status = Service.Status.ACCEPTED if is_accepted else Service.Status.REJECTED
    db_service.estimate_arrival_at = estimate_arrival_at
    db_service.updated_at = timezone.now()
    db_service.updated_by = user
    db_service._custom_remark = _("Service accepted by the technician.") if is_accepted else _("Service rejected by the technician.")

    # Update the service's reject reason if the service is rejected
    if not is_accepted:
        db_service._custom_remark = _("Service rejected by the technician. Reason:") + reject_reason if reject_reason else _("Service rejected by the technician.")

    db_service.full_clean()
    db_service.save()
