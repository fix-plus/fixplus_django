from enum import Enum

from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address


class Service(BaseModel, SoftDeleteBaseModel):
    WAITING = 'waiting'
    ASSIGNED = 'assigned'
    ACCEPTED = 'accepted'
    REFERRED_TO_SHOP = 'referred_to_shop'
    INVOICING = 'invoicing'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    EXPIRED = 'expired'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (WAITING, 'Waiting for Assign'),
        (ASSIGNED, 'Assigned'),
        (ACCEPTED, 'Accepted'),
        (REFERRED_TO_SHOP, 'Referred to Shop'),
        (INVOICING, 'Invoicing'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
        (EXPIRED, 'Expired'),
        (CANCELED, 'Canceled'),
    ]

    # Core
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING)
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
    reason_arrival_delayed = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.full_name} : {self.brand}-{self.device_type}"