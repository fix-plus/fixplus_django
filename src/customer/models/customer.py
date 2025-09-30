from django.db import models

from src.common.models import BaseModel


class Customer(BaseModel):
    class Gender(models.TextChoices):
        FEMALE = 'FEMALE', 'Female'
        MALE = 'MALE', 'Male'

    subscription_code = models.IntegerField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        if not self.subscription_code:
            last_customer = Customer.objects.all().order_by('subscription_code').last()
            if last_customer and last_customer.subscription_code:
                self.subscription_code = last_customer.subscription_code + 1
            else:
                self.subscription_code = 110001
        super().save(*args, **kwargs)