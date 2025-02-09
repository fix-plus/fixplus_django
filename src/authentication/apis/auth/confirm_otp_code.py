from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.account.selectors.user import get_tokens_user, get_user
from src.account.serializers.auth import InputConfirmVerificationCodeSerializer, OutPutTokensUserSerializer
from src.account.services.user import update_verified
from src.account.utils import verify_otp


class ConfirmOtpCodeApi(APIView):
    @extend_schema(
        summary="Confirm Verification Code",
        request=InputConfirmVerificationCodeSerializer,
        responses=OutPutTokensUserSerializer)
    def post(self, request):
        serializer = InputConfirmVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validation
        if verify_otp(
                mobile=serializer.validated_data.get("mobile"),
                code=serializer.validated_data.get("code")
        ):
            user = get_user(mobile=serializer.validated_data.get("mobile"))

            # Core
            if not user.is_verified_mobile:
                update_verified(
                    mobile=serializer.validated_data.get("mobile"),
                    code=serializer.validated_data.get("code")
                )

        # Response
        tokens_data = get_tokens_user(mobile=serializer.validated_data.get("mobile"))
        return Response(OutPutTokensUserSerializer(tokens_data).data, status=status.HTTP_200_OK)



