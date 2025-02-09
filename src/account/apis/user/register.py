from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsVerifiedMobileMixin
from src.account.services.register import update_register


class RegisterApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Register",
    )
    def get(self, request):
        with transaction.atomic():
            update_register(user=request.user)

        return Response({'result': _('The request was sent successfully.')},
                        status=status.HTTP_200_OK)
