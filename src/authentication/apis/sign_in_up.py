from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.authentication.selectors.auth import get_cache_verification_mobile_otp
from src.common.custom_exception import CustomAPIException
from src.authentication.serializers.auth import InputSignInUpSerializer
from src.authentication.services.auth import get_or_create_user, set_cache_verification_mobile_otp
from src.authentication.tasks import send_verification_sms
from src.authentication.utils import generate_otp_code


class SignInUpApi(APIView):
    @extend_schema(
        summary="Sign In/Up ",
        request=InputSignInUpSerializer)
    def post(self, request):
        serializer = InputSignInUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if get_cache_verification_mobile_otp(mobile=serializer.validated_data.get("mobile")) is None:
            user = get_or_create_user(mobile=serializer.validated_data.get("mobile"), )

            # Send Otp Verification
            otp_code = generate_otp_code()
            print(otp_code)  # TODO: It's Should be Remove!!!

            data = {
                'receptor': serializer.validated_data.get("mobile"),
                'template': 'otp',
                'otp_code': otp_code,
            }

            send_verification_sms.delay(data)

            set_cache_verification_mobile_otp(mobile=serializer.validated_data.get("mobile"), otp=otp_code)

            return Response({'result': _('A verification code has been send to your mobile number.')}, status=status.HTTP_200_OK)

        else:
            raise CustomAPIException(message=_('2 minutes must have passed since the last sms was sent.'), status_code=status.HTTP_408_REQUEST_TIMEOUT)
