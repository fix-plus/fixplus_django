import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from fixplus.common.models import BaseModel
from fixplus.upload.validators import FileSizeValidator, ImageSizeValidator
from fixplus.user.models import BaseUser


def upload_image_identify_document(instance, filename):
    return 'images/identify-document/{filename}.{format}'.format( filename=str(uuid.uuid4()), format=filename.split(".")[-1])


class UploadIdentifyDocumentMedia(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=upload_image_identify_document,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            FileSizeValidator(min_size=1, max_size=5 * 1024 * 1024),
            ImageSizeValidator(max_height=4000, min_height=300, max_width=3000, min_width=300)
        ],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Identify Document Medias"
        verbose_name_plural = "Identify Document Medias"

    def __str__(self):
        return f"{self.id}"