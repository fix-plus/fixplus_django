from django.shortcuts import redirect, render
from django.urls import reverse
from azbankgateways.exceptions import AZBankGatewaysException
from src.payment.services.online_payment import verify_online_payment
import logging

logger = logging.getLogger(__name__)

def payment_callback(request):
    """
    Handle callback from Zarinpal after payment.
    """
    logger.info(f"Callback received with query params: {request.GET}")
    tracking_code = request.GET.get('Authority') or request.GET.get('tracking_code')
    logger.info(f"Payment callback received with tracking code: {tracking_code}")

    if not tracking_code:
        logger.error("No tracking code provided in callback")
        return redirect(reverse('payment-result') + '?status=failure&tracking_code=N/A')

    try:
        check_verified = verify_online_payment(tracking_code)
        bank_record = check_verified['bank_record']
        paid_with = check_verified['paid_with']
        logger.info(f"Verification result for {tracking_code}: is_success={bank_record.is_success}")
        if bank_record.is_success:
            logger.info(f"Payment successful for tracking code: {tracking_code}")
            if paid_with == 'TECHNICIAN':
                return redirect(reverse('technician-payment-result') + f'?status=success&tracking_code={tracking_code}')
            elif paid_with == 'CUSTOMER':
                return redirect(reverse('customer-payment-result') + f'?status=success&tracking_code={tracking_code}')
        else:
            logger.warning(f"Payment failed for tracking code: {tracking_code}")
            return redirect(reverse('payment-result') + f'?status=failure&tracking_code={tracking_code}')
    except AZBankGatewaysException as e:
        logger.error(f"Payment verification failed for {tracking_code}: {str(e)}")
        return redirect(reverse('payment-result') + f'?status=failure&tracking_code={tracking_code}')


def technician_payment_result(request):
    """
    Render the payment result page.
    """
    status = request.GET.get('status', 'failure')
    tracking_code = request.GET.get('tracking_code', 'N/A')
    logger.info(f"Rendering payment result: status={status}, tracking_code={tracking_code}")
    return render(request, 'technician_payment_result.html', {'status': status, 'tracking_code': tracking_code})


def customer_payment_result(request):
    """
    Render the payment result page.
    """
    status = request.GET.get('status', 'failure')
    tracking_code = request.GET.get('tracking_code', 'N/A')
    logger.info(f"Rendering payment result: status={status}, tracking_code={tracking_code}")
    return render(request, 'customer_payment_result.html', {'status': status, 'tracking_code': tracking_code})