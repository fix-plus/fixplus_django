from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.custom_exception import CustomAPIException
from src.financial.services.invoice_deduction import add_invoice_deduction_items
from src.service.models import Service


def create_invoice_deduction(
        *,
        technician: User,
        service: Service,
        ignored_system_fee: bool = None,
        other_invoice_deduction_description: str = None,
        deduction_items = None,
) -> Service:
    # Check Technician of this Service is the same as the user
    if service.technician != technician:
        raise CustomAPIException(_("This service is not assigned to the technician."), status_code=406)

    if ignored_system_fee == True:
        service.status = Service.Status.IGNORED_SYSTEM_FEE_INVOICING
        service.save()
        return service

    if deduction_items is not None:
        for item in deduction_items:
            add_invoice_deduction_items(
                service=service,
                description=item['description'],
                cost=item['cost'],
                quantity=item['quantity'],
            )

    if other_invoice_deduction_description is not None:
        service.other_invoice_deduction_description = other_invoice_deduction_description
        service.save()

    service.status = Service.Status.SYSTEM_FEE_PAYMENT
    service.save()

    return service