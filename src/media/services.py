from django.db.models import ImageField, UUIDField, FileField

from src.common.custom_exception import CustomAPIException
from src.media.models import UploadIdentifyDocumentMedia
from src.authentication.models import User


def create_upload_identify_document_media(*, user:User, id: str=None, image: ImageField | None = None) -> UploadIdentifyDocumentMedia:
    if image:
        return UploadIdentifyDocumentMedia.objects.create(user= user, id=id, image=image)
    else:
        raise CustomAPIException()