from src.financial.models.invoice_deduction_item import InvoiceDeductionItem
from src.service.models import Service


def add_invoice_deduction_items(
        *,
        service: Service,
        description: str,
        cost: int,
        quantity: int,
        **kwargs
) -> InvoiceDeductionItem:
    deduction = InvoiceDeductionItem(
        service=service,
        description=description,
        cost=cost,
        quantity=quantity,
        **kwargs,
    )
    deduction.full_clean()
    deduction.save()
    return deduction