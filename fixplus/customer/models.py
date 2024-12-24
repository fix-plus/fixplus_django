from django.db import models

from fixplus.common.models import SoftDeleteBaseModel
from fixplus.user.models import BaseUser


class Customer(SoftDeleteBaseModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    added_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='customer_added_by', null=True, editable=False)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    class Meta:
        pass

    def __str__(self):
        return f"{self.full_name}"


class CustomerPhoneNumber(SoftDeleteBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.full_name} : {self.number}"