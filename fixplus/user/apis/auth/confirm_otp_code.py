from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fixplus.user.selectors.user import get_tokens_user, get_user
from fixplus.user.serializers.auth import InputConfirmVerificationCodeSerializer,  OutputTokensUserSerializer
from fixplus.user.services.user import update_verified
from fixplus.user.utils import verify_otp


class ConfirmOtpCodeApi(APIView):
    @extend_schema(
        summary="Confirm Verification Code",
        request=InputConfirmVerificationCodeSerializer,
        responses=OutputTokensUserSerializer)
    def post(self, request):
        serializer = InputConfirmVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if verify_otp(
                mobile=serializer.validated_data.get("mobile"),
                code=serializer.validated_data.get("code")
            ):
                user = get_user(mobile=serializer.validated_data.get("mobile"))

                if not user.is_verified_mobile:
                    update_verified(
                        mobile=serializer.validated_data.get("mobile"),
                        code=serializer.validated_data.get("code")
                    )

            tokens_data = get_tokens_user(mobile=serializer.validated_data.get("mobile"))

        except Exception as e:
            return Response(
                {'detail': f"{e}"},
                 status= status.HTTP_400_BAD_REQUEST
            )

        else:
            return Response(OutputTokensUserSerializer(tokens_data).data, status=status.HTTP_200_OK)



