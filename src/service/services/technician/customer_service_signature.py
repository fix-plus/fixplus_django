from django.db import transaction
from django.db.models import ImageField, UUIDField, FileField

from src.common.custom_exception import CustomAPIException
from src.media.models import UploadIdentifyDocumentMedia, UploadServiceCardMedia
from src.authentication.models import User
from src.media.models.customer_signature import UploadCustomerSignatureMedia
from src.service.models import Service, CustomerServiceSignature


@transaction.atomic
def create_customer_service_signature(
        *,
        service: Service,
        image: UploadCustomerSignatureMedia,

) -> CustomerServiceSignature:
    customer_service_signature = CustomerServiceSignature.objects.create(
        service=service,
        media=image,
    )

    service.status = Service.Status.CUSTOMER_SIGNATURE
    service.save()

    return customer_service_signature