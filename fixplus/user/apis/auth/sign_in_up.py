from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fixplus.user.selectors.user import get_cache_verification_mobile_otp
from fixplus.user.serializers.auth import InputSignInUpSerializer
from fixplus.user.services.user import create_user, set_cache_verification_mobile_otp

from fixplus.user.tasks import send_verification_sms
from fixplus.user.utils import generate_otp_code


class SignInUpApi(APIView):
    @extend_schema(
        summary="Sign In/Up ",
        request=InputSignInUpSerializer)
    def post(self, request):
        serializer = InputSignInUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                if get_cache_verification_mobile_otp(mobile=serializer.validated_data.get("mobile")) is None:
                    user = create_user(
                        mobile=serializer.validated_data.get("mobile"),
                    )

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

                    return Response({'result': 'The user has been successfully created, please check mobile inbox.'},
                                    status=status.HTTP_200_OK)

                else:
                    return Response({'detail': '2 minutes must have passed since the last sms was sent.'},
                                    status=status.HTTP_408_REQUEST_TIMEOUT)

        except Exception as e:
            return Response(
                {'detail': f"{e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
