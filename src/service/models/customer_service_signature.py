from django.db import models

from src.common.models import BaseModel
from src.media.models.customer_signature import UploadCustomerSignatureMedia
from src.service.models.service import Service


class CustomerServiceSignature(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='customer_service_signatures', null=False, blank=False)
    media = models.ForeignKey(UploadCustomerSignatureMedia, on_delete=models.CASCADE, related_name='customer_service_signatures', null=False, blank=False)

    def __str__(self):
        return f"{self.service}"