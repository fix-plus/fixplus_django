from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.customer.models import Customer
from src.service.models.job import Job
from src.authentication.models import User


class PartInShop(BaseModel, SoftDeleteBaseModel):
    STATUS_CHOICES = [
        ('in_progress', "In Progress"),
        ('completed', "Completed"),
    ]

    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.PROTECT,
        related_name='parts_in_shop',
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='parts_in_shop',
        null=True,
        blank=True,
    )
    technician = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='parts_in_shop',
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

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.title}"
