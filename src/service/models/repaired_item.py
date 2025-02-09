from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.job import Job
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class RepairedItem(BaseModel, SoftDeleteBaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='repaired_items',
        null=True,
        blank=True,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.PROTECT,
        related_name='repaired_items',
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    cost = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.title}"