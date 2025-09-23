import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel
from src.media.validators import FileSizeValidator, ImageSizeValidator


def upload_image_customer_signature_document(instance, filename):
    return 'images/signature/customer/{filename}.{format}'.format( filename=str(uuid.uuid4()), format=filename.split(".")[-1])


class UploadCustomerSignatureMedia(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_signature_medias')
    image = models.ImageField(
        upload_to=upload_image_customer_signature_document,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            FileSizeValidator(min_size=1, max_size=5 * 1024 * 1024),
            ImageSizeValidator(max_height=4000, min_height=300, max_width=3000, min_width=300)
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"