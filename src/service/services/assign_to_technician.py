from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.account.models import TechnicianStatus
from src.authentication.models import User
from src.authentication.selectors.auth import get_user
from src.common.custom_exception import CustomAPIException
from src.parametric.selectors.selectors import get_timing_setting
from src.service.models import Service
from src.service.selectors.service import get_service


def assign_service_to_technician(
        *,
        service_id: str,
        technician_id: str,
        assigned_by: User,
):
    db_service = get_service(id=service_id)
    db_technician = get_user(id=technician_id)

    # Check if the service is already assigned to the technician
    if db_service.technician == db_technician : raise CustomAPIException(_("Service is already assigned to the technician"), status_code=400)

    # Check if the service is already completed
    if db_service.status == Service.COMPLETED: raise CustomAPIException(_("Service is already completed"), status_code=400)

    # Check if technician not active
    if db_technician.technician_statuses.latest('created_at').status != TechnicianStatus.ACTIVE: raise CustomAPIException(_("Technician is not active"), status_code=400)

    # Initial
    timing_setting_db = get_timing_setting()

    # Update and assign the service to the technician
    db_service.technician = db_technician
    db_service.updated_at = timezone.now()
    db_service.updated_by = assigned_by
    db_service.status = Service.ASSIGNED
    db_service.deadline_accepting_at = timezone.now() + timezone.timedelta(minutes=timing_setting_db.max_wait_determine_referred_job_by_tech_min)
    db_service._custom_remark = "Service assigned to the technician."

    db_service.full_clean()
    db_service.save()


    return db_service