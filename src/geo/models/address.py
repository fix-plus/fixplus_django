from django.utils.translation import gettext_lazy as _
from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel
from src.customer.models import Customer


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.user is None and self.customer is None:
            raise ValueError(_("Either user or customer must be provided for the address."))

    def __str__(self):
        return self.address