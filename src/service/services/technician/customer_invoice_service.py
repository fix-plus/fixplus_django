from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException
from src.financial.models import CustomerInvoice
from src.financial.services.invoice_generator import generate_invoice_pdf
from src.service.models import Service
from src.service.selectors.service import get_service


def customer_invoice_service(
    *,
    request: Request,
    service_id:  str,
    technician: User,
    completed_service_items = None,
    discount_amount: int = 0,
    warranty_period_id: str = None,
    warranty_description: str = None,
    wage_cost: int = 0,
    deadheading_cost: int = 0,
    **kwargs,
):
    db_service = get_service(id=service_id)

    # Check Technician of this Service is the same as the user
    if db_service.technician != technician:
        raise CustomAPIException(_("This service is not assigned to the technician."), status_code=406)

    # Check Service is in correct status
    if db_service.status != Service.Status.ACCEPTED:
        raise CustomAPIException(_("Service is not in the correct status to be continue this function."), status_code=400)

    # Add Completed Service Items
    if completed_service_items:
        from src.service.services.technician.completed_service_item import add_completed_service_item
        for item in completed_service_items:
            add_completed_service_item(
                service=db_service,
                description=item['description'],
                cost=item['cost'],
                quantity=item['quantity'],
            )

    # Get Warranty Period
    warranty_period = None
    if warranty_period_id:
        from src.parametric.selectors.warranty_period import get_warranty_period
        warranty_period = get_warranty_period(id=warranty_period_id)

    # Update Customer Invoice
    db_customer_invoice, is_new = CustomerInvoice.objects.get_or_create(
        service=db_service,
        defaults={
            'warranty_period': warranty_period,
            'warranty_description': warranty_description,
            'discount_amount': discount_amount,
            'wage_cost': wage_cost,
            'deadheading_cost': deadheading_cost,
        }
    )

    # Update Service
    db_service.status = Service.Status.CUSTOMER_INVOICING

    db_service.full_clean()
    db_service.save()

    # Generate PDF
    generate_invoice_pdf(invoice_id=db_customer_invoice.id, request=request)
