from django.db.models import ImageField, UUIDField, FileField

from src.common.custom_exception import CustomAPIException
from src.media.models import UploadIdentifyDocumentMedia, UploadServiceCardMedia
from src.authentication.models import User
from src.media.models.customer_signature import UploadCustomerSignatureMedia


def create_upload_identify_document_media(*, user:User, id: str=None, image: ImageField | None = None) -> UploadIdentifyDocumentMedia:
    if image:
        return UploadIdentifyDocumentMedia.objects.create(user= user, id=id, image=image)
    else:
        raise CustomAPIException()


def create_upload_service_card_media(*, user:User, id: str=None, image: ImageField | None = None) -> UploadServiceCardMedia:
    if image:
        return UploadServiceCardMedia.objects.create(user= user, id=id, image=image)
    else:
        raise CustomAPIException()


def create_upload_customer_signature_media(*, user:User, id: str=None, image: ImageField | None = None) -> UploadCustomerSignatureMedia:
    if image:
        return UploadCustomerSignatureMedia.objects.create(user= user, id=id, image=image)
    else:
        raise CustomAPIException()