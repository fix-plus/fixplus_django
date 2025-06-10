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