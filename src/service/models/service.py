from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from jedi.inference.flow_analysis import Status

from src.authentication.models import User
from src.common.models import BaseModel
from src.customer.models import Customer
from src.media.models.customer_signature import UploadCustomerSignatureMedia
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address


class Service(BaseModel):
    class Status(models.TextChoices):
        WAITING = 'WAITING', 'Waiting'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        CUSTOMER_INVOICING = 'CUSTOMER_INVOICING', 'Customer Invoicing'
        CUSTOMER_PAYMENT = 'CUSTOMER_PAYMENT', 'Customer Payment'
        CUSTOMER_SIGNATURE = 'CUSTOMER_SIGNATURE', 'Customer Signature'
        IGNORED_SYSTEM_FEE_INVOICING = 'IGNORED_SYSTEM_FEE_INVOICING', 'Ignored System Fee Invoicing'
        SYSTEM_FEE_INVOICING = 'SYSTEM_FEE_INVOICING', 'System Fee Invoicing'
        SYSTEM_FEE_PAYMENT = 'SYSTEM_FEE_PAYMENT', 'System Fee Payment'
        COMPLETED = 'COMPLETED', 'Completed'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELED = 'CANCELED', 'Canceled'

    # Core
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.WAITING)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="services", on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, null=False, blank=False, on_delete=models.CASCADE, related_name="services")
    brand = models.ForeignKey(Brand, null=False, blank=False, on_delete=models.CASCADE, related_name="services")
    customer_description = models.TextField(blank=True, null=True)
    description_for_technician = models.TextField( blank=True, null=True)
    address = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name="services")

    # Assigned
    technician = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="services")
    deadline_accepting_at = models.DateTimeField(null=True, blank=True)

    # Accepted
    estimate_arrival_at = models.DateTimeField(null=True, blank=True)

    # Customer Signature
    customer_signature = models.ForeignKey(UploadCustomerSignatureMedia, null=True, blank=True, on_delete=models.SET_NULL, related_name="services")

    # System Fee Invoicing
    other_completed_service_description = models.TextField(blank=True, null=True)

    # Rejected
    reject_reason = models.TextField(blank=True, null=True)

    # Expired
    expired_reason = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.customer.full_name} : {self.brand}-{self.device_type}"

    def set_expired(self, custom_remark=None):
        self.status = Service.Status.EXPIRED
        self._custom_remark = custom_remark or _("Service expired.")
        self.updated_at = timezone.now()
        self.technician = None
        self.deadline_accepting_at = None
        self.estimate_arrival_at = None
        self.save()