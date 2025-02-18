from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer


class CustomerContactNumber(BaseModel, SoftDeleteBaseModel):
    PHONE_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('landline', 'Landline'),
    ]

    customer = models.ForeignKey(
        Customer,
        related_name='contact_numbers',
        on_delete=models.CASCADE
    )
    phone_type = models.CharField(
        max_length=8,
        choices=PHONE_TYPE_CHOICES
    )
    number = models.CharField(
        max_length=15
    )
    is_primary = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if self.is_primary:
            CustomerContactNumber.objects.filter(user=self.customer, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} ({self.get_phone_type_display()})"

    class Meta:
        unique_together = ('customer', 'number')