from django.utils.translation import gettext_lazy as _
from django.db import models

from src.common.models import BaseModel
from src.common.utils import to_jalali_date_string
from src.parametric.models import WarrantyPeriod
from src.service.models.service import Service


def get_invoice_upload_path(instance, filename):
    return 'invoices/service/{filename}.{format}'.format( filename=instance.service.id, format='pdf')


class CustomerInvoice(BaseModel):
    identify_code = models.IntegerField(unique=True, null=True, blank=True)
    service = models.OneToOneField(Service, null=False, blank=False, on_delete=models.CASCADE, related_name='customer_invoice')
    warranty_period = models.ForeignKey(WarrantyPeriod, null=True, blank=True, on_delete=models.PROTECT)
    warranty_description = models.TextField(null=True, blank=True)
    discount_amount = models.PositiveBigIntegerField(null=False, blank=False, default=0)
    wage_cost = models.PositiveBigIntegerField(null=False, blank=False)
    deadheading_cost = models.PositiveBigIntegerField(null=False, blank=False)
    pdf_output = models.FileField(upload_to=get_invoice_upload_path, null=True, blank=True, max_length=500)

    def __str__(self):
        return f"{self.service}"

    def save(self, *args, **kwargs):
        if not self.identify_code:
            last_invoice = CustomerInvoice.objects.all().order_by('identify_code').last()
            if last_invoice and last_invoice.identify_code:
                self.identify_code = last_invoice.identify_code + 1
            else:
                self.identify_code = 500001
        super().save(*args, **kwargs)

    def get_total_invoice_amount(self):
        """
        Calculate the total invoice amount by summing wage_cost, deadheading_cost,
        and the total cost of all related CompletedServiceItems (cost * quantity).
        """
        completed_items_total = sum(
            item.cost * item.quantity
            for item in self.service.completed_service_items.all()
        )
        return self.wage_cost + self.deadheading_cost + completed_items_total

    def get_payable_amount(self):
        """
        Calculate the payable amount by subtracting the discount_amount
        from the total invoice amount.
        """
        return self.get_total_invoice_amount() - self.discount_amount

    def get_total_invoice_deduction_amount(self):
        return sum(item.cost * item.quantity for item in self.service.invoice_deduction_items.all()) if self.service.invoice_deduction_items.exists() else 0

    def get_system_fee(self):
        return (self.get_payable_amount() - self.get_total_invoice_deduction_amount()) * 0.5

    def get_notes(self):
        # Start date in Jalali format
        start_date = to_jalali_date_string(self.created_at, '%Y/%m/%d')

        # Warranty details
        warranty_text = ""
        if self.warranty_period:
            warranty_text = f"{self.warranty_period.duration} {self.warranty_period.get_time_unit_display()}"
            if self.warranty_description:
                warranty_text += f" {self.warranty_description}"

        # Subscription code from customer
        subscription_code = self.service.customer.subscription_code or ""

        # Technician details
        technician_name = self.service.technician.profile.full_name if self.service.technician else ""
        technician_identity_code = self.service.technician.identity_code if self.service.technician else ""

        # Construct the final string
        return (
            f"شروع گارانتی از تاریخ : {start_date}   |   "
            f"گارانتی : {warranty_text}   |   "
            f"اشتراک : {subscription_code}   |   "
            f"تکنسین : آقای {technician_name}   |   "
            f"کد تکنسین : {technician_identity_code}"
        )