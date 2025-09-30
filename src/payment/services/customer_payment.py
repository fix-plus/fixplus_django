from django.utils.translation import gettext_lazy as _
from azbankgateways.models import Bank, PaymentStatus

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException
from src.payment.models import CustomerPayment
from src.payment.services.online_payment import initiate_customer_online_payment
from src.service.models import Service


def create_customer_payment(
        *,
        request,
        technician: User,
        service: Service,
        cheque_amount: int = None,
        cash_amount: int = None,
        card_to_card_amount: int = None,
        online_amount: int = None,
        online_phone_number: str = None,
        **kwargs,
) -> CustomerPayment:
    # Validate Service Technician is equal to technician
    if technician != service.technician:
        raise CustomAPIException(_("Technician is not valid."))

    # Validate Service status
    if service.status != Service.Status.CUSTOMER_INVOICING:
        raise CustomAPIException(_("Service status is not valid for customer payment."))

    # Try to get or create CustomerPayment based on service and technician
    customer_payment, is_created = CustomerPayment.objects.get_or_create(
        service=service,
        technician=technician,
        defaults={
            'cheque_amount': cheque_amount or 0,
            'cash_amount': cash_amount or 0,
            'card_to_card_amount': card_to_card_amount or 0,
            'online_amount': online_amount or 0,
        }
    )

    # If the record already exists, update the fields
    if not is_created:
        # Update only the provided fields
        if cheque_amount is not None:
            customer_payment.cheque_amount = cheque_amount
        if cash_amount is not None:
            customer_payment.cash_amount = cash_amount
        if card_to_card_amount is not None:
            customer_payment.card_to_card_amount = card_to_card_amount
        customer_payment.save()

    # Handle online payment if online_amount is provided
    if online_amount:
        initiate_customer_online_payment(
            customer_payment=customer_payment,
            amount=online_amount,
            customer_phone_number=online_phone_number,
            request=request,
        )
    else:
        # Update service status
        service = customer_payment.service
        service.status = Service.Status.CUSTOMER_PAYMENT
        service.save()

    return customer_payment


def verify_customer_payment_with_online(
        *,
        technician: User,
        service: Service,
) -> CustomerPayment:
    try:
        customer_payment = CustomerPayment.objects.filter(technician=technician, service=service).first()
    except CustomerPayment.DoesNotExist:
        raise CustomAPIException(_("Customer payment does not exist."))

    if not customer_payment.online_bank:
        raise CustomAPIException(_("No online payment to verify."))

    if customer_payment.online_bank.status == PaymentStatus.COMPLETE:
        service = customer_payment.service
        service.status = Service.Status.CUSTOMER_PAYMENT
        service.save()

    return customer_payment
