from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address


class Job(BaseModel, SoftDeleteBaseModel):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Assign'),
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('referred_to_shop', 'Referred to Shop'),
        ('invoicing', 'Invoicing'),
        ('pay_invoice', 'Wait For Pay Invoice'),
        ('pay_fee', 'Waiting for Pay System Fee'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )
    customer = models.ForeignKey(
        Customer,
        null=False,
        blank=False,
        related_name="customer",
        on_delete=models.PROTECT
    )
    device_type = models.ForeignKey(
        DeviceType,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    brand_name = models.ForeignKey(
        Brand,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    customer_description = models.TextField(
        blank=True,
        null=True
    )
    description_for_technician = models.TextField(
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        Address,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.customer.full_name} : {self.brand_name}-{self.device_type}"