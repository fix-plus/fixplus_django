from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsVerifiedMobileMixin
from fixplus.user.services.register import update_register


class RegisterApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Register",
    )
    def get(self, request):
        try:
            with transaction.atomic():
                update_register(user=request.user)

            return Response({'result': _('The request was sent successfully.')},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': f"{e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
