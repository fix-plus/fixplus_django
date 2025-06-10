from src.account.models import TechnicianStatus
from src.authentication.models import User


def get_latest_technician_status(*, user:User):
    # Create init status if it doesn't exist
    if not user.technician_statuses.exists():
        TechnicianStatus.objects.create(user=user, status=TechnicianStatus.Status.ACTIVE)
    return user.technician_statuses.latest('created_at') if user.technician_statuses.exists() else None