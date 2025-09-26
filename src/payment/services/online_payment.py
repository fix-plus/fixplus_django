import logging

from azbankgateways.models import Bank
from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from azbankgateways import bankfactories, models as bank_models
from azbankgateways.exceptions import AZBankGatewaysException
from src.common.custom_exception import CustomAPIException
from src.authentication.models import User
from src.payment.models import CustomerPayment, TechnicianPayment
from src.service.selectors.service import get_service
from src.payment.tasks import send_online_payment_sms

logger = logging.getLogger(__name__)


@transaction.atomic
def initiate_customer_online_payment(
        *,
        technician: User,
        service_id: str,
        amount: int,
        customer_phone_number: str,
        request,
) -> dict:
    service = get_service(id=service_id)
    factory = bankfactories.BankFactory()

    try:
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.set_mobile_number(customer_phone_number or '+989000000000')
        bank_record = bank.ready()

        customer_payment = service.customer_payments.filter(technician=technician).latest("-created_at")
        customer_payment.online_bank = bank_record
        customer_payment.online_amount = amount
        customer_payment.online_phone_number = customer_phone_number
        customer_payment.save()

        context = bank.get_gateway()
        is_sandbox = bool(settings.AZ_IRANIAN_BANK_GATEWAYS.get('GATEWAYS')[bank.get_bank_type()].get('SANDBOX'))

        # Send SMS to customer
        sms_context = context['url'].replace('https://sandbox.zarinpal.com/', '') if is_sandbox else context['url'].replace('https://payment.zarinpal.com/', '')
        sms_data = {
            'receptor': customer_phone_number,
            'customer_name': 'آقای پیمان میرانشاهی',
            'amount': amount,
            'url_context': sms_context,
            'template': 'sandboxCustomerPaymentUrl' if is_sandbox else 'customerPaymentUrl'
        }
        send_online_payment_sms.delay(sms_data)

        return context
    except AZBankGatewaysException as e:
        logger.error(f"Payment initiation failed: {str(e)}")
        raise CustomAPIException(_('Failed to initiate payment.'), status.HTTP_500_INTERNAL_SERVER_ERROR)


@transaction.atomic
def verify_online_payment(tracking_code: str) -> dict | None:
    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logger.error(f"Invalid tracking code: {tracking_code}")
        raise CustomAPIException(_('Invalid tracking code.'), status.HTTP_404_NOT_FOUND)

    if bank_record.is_success:
        customer_payment = CustomerPayment.objects.filter(online_bank=bank_record)
        technician_payment = TechnicianPayment.objects.filter(online_bank=bank_record)

        if technician_payment.exists():
            technician_payment = technician_payment.first()
            technician_internal_wallet = technician_payment.technician.internal_wallet
            technician_internal_wallet.balance += bank_record.amount
            technician_internal_wallet.save()
            return {
                'paid_with': 'TECHNICIAN',
                'bank_record': bank_record,
            }

        elif customer_payment.exists():
            customer_payment = customer_payment.first()
            technician_internal_wallet = customer_payment.technician.internal_wallet
            technician_internal_wallet.balance += int(bank_record.amount)
            technician_internal_wallet.save()
            return {
                'paid_with': 'CUSTOMER',
                'bank_record': bank_record,
            }