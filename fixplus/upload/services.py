from django.db.models import ImageField, UUIDField, FileField

from fixplus.upload.models import UploadIdentifyDocumentMedia
from fixplus.user.models import BaseUser


def create_upload_identify_document_media(*, user:BaseUser, id: str=None, image: ImageField | None = None) -> UploadIdentifyDocumentMedia:
    if image:
        return UploadIdentifyDocumentMedia.objects.create(user= user, id=id, image=image)
    else:
        raise Exception("Unknown error occurred.")