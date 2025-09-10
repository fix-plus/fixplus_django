from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.mixins import IsVerifiedMobileMixin
from src.account.selectors.profile import get_profile
from src.account.serializers.shared.profile import OutPutProfileSerializer, InputUpdateProfileSerializer
from src.account.services.profile import update_profile


class MeApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Get Profile",
        responses=OutPutProfileSerializer)
    def get(self, request):
        db_user_profile = get_profile(user=request.user)

        return Response(OutPutProfileSerializer(db_user_profile, context={"request": request}, user_type='me').data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Profile",
        request=InputUpdateProfileSerializer,
        responses=OutPutProfileSerializer)
    def patch(self, request):
        serializer = InputUpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_user_profile = update_profile(
            request.user.profile,
            **serializer.validated_data
        )

        return Response(OutPutProfileSerializer(db_user_profile, context={"request": request}, user_type='me').data, status=status.HTTP_200_OK)