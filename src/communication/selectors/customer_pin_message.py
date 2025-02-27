from src.communication.models import CustomerPinMessage
from src.customer.models import Customer


def get_latest_customer_pin_message(*, customer: Customer):
    """
    Get customer pin message
    """
    try:
        return CustomerPinMessage.objects.filter(customer=customer).latest('-created_at')
    except CustomerPinMessage.DoesNotExist:
        return CustomerPinMessage.objects.none()