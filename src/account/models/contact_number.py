from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.authentication.models import User


class UserContactNumber(BaseModel, SoftDeleteBaseModel):
    MOBILE = 'mobile'
    LAND_LINE = 'landline'

    PHONE_TYPE_CHOICES = [
        (LAND_LINE, 'Mobile'),
        (MOBILE, 'Landline')
    ]

    user = models.ForeignKey(User, related_name='contact_numbers', on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=8, choices=PHONE_TYPE_CHOICES)
    number = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            UserContactNumber.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} ({self.get_phone_type_display()})"

    class Meta:
        unique_together = ('user', 'number')