from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.authentication.serializers.auth import InputReSendVerificationCodeSerializer
from src.common.custom_exception import CustomAPIException
from src.authentication.selectors.auth import is_exist_user, get_cache_verification_mobile_otp
from src.authentication.services.auth import set_cache_verification_mobile_otp
from src.authentication.utils import generate_otp_code
from src.authentication.tasks import send_verification_sms


class ReSendOtpCodeApi(APIView):
    @extend_schema(
        summary="Re-Send Verification Code",
        request=InputReSendVerificationCodeSerializer)
    def post(self, request):
        serializer = InputReSendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data.get("mobile")

        if not is_exist_user(mobile=mobile):
            raise  CustomAPIException(message=_('User with this mobile not found.'), status_code=status.HTTP_404_NOT_FOUND)

        if get_cache_verification_mobile_otp(mobile=mobile) is None:
            otp_code = generate_otp_code()

            print(otp_code)  # TODO: It's Should be Remove!!!
            data = {
                'receptor': serializer.validated_data.get("mobile"),
                'template': 'otp',
                'otp_code': otp_code,
            }

            send_verification_sms.delay(data)

            set_cache_verification_mobile_otp(mobile=mobile, otp=otp_code)
            return Response({'result': _('A verification code has been send to your mobile number.')}, status=status.HTTP_200_OK)

        else:
            raise CustomAPIException(message=_('2 minutes must have passed since the last sms was sent.'), status_code=status.HTTP_408_REQUEST_TIMEOUT)



