from src.authentication.models import User
from src.communication.models import AdminPinMessageOfTechnician


def get_latest_admin_pin_message_of_technician(*, user: User):
    try:
        return AdminPinMessageOfTechnician.objects.filter(user=user).latest('created_at')
    except AdminPinMessageOfTechnician.DoesNotExist:
        return None