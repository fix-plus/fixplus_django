from django.db.models import OuterRef, Subquery
from  django.utils.translation import gettext_lazy as _

from src.account.models import TechnicianStatus
from src.account.selectors.technician_status import get_latest_technician_status
from src.authentication.models import User
from src.common.custom_exception import CustomAPIException


def create_technician_status(*, user: User, status: TechnicianStatus.Status):
    # check user is TECHNICIAN
    if not user.groups.filter(name='TECHNICIAN').exists():
        raise CustomAPIException(_("This method only active for technician users."), status_code=403)

    if get_latest_technician_status(user=user).status == status:
        return get_latest_technician_status(user=user)
    return TechnicianStatus.objects.create(user=user, status=status)


def get_active_technicians():
    # Subquery to get the latest TechnicianStatus for each user
    latest_status = TechnicianStatus.objects.filter(
        user=OuterRef('pk'),
        is_deleted=False
    ).order_by('-created_at')[:1]

    # Return users whose latest status is ACTIVE and are in the TECHNICIAN group
    return User.objects.filter(
        technician_statuses__is_deleted=False,
        technician_statuses__status=TechnicianStatus.Status.ACTIVE,
        groups__name='TECHNICIAN'
    ).annotate(
        latest_status=Subquery(latest_status.values('status'))
    ).filter(
        latest_status=TechnicianStatus.Status.ACTIVE
    ).distinct()