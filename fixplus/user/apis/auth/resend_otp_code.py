from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.user.selectors.user import is_exist_user, get_cache_verification_mobile_otp
from fixplus.user.serializers.auth import InputReSendVerificationCodeSerializer
from fixplus.user.services.user import set_cache_verification_mobile_otp
from fixplus.user.utils import generate_otp_code
from fixplus.user.tasks import send_verification_sms


class ReSendOtpCodeApi(APIView):
    @extend_schema(
        summary="Re-Send Verification Code",
        request=InputReSendVerificationCodeSerializer)
    def post(self, request):
        serializer = InputReSendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data.get("mobile")

        if not is_exist_user(mobile=mobile):
            return Response({'detail': _('User with this mobile not found.')}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'detail': _('2 minutes must have passed since the last sms was sent.')},
                            status=status.HTTP_408_REQUEST_TIMEOUT)



