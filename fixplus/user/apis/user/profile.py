from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fixplus.common.mixins import IsVerifiedMobileMixin
from fixplus.user.selectors.profile import get_profile
from fixplus.user.serializers.profile import OutPutProfileSerializer, InputUpdateProfileSerializer
from fixplus.user.services.profile import update_profile


class ProfileApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Get Profile",
        responses=OutPutProfileSerializer)
    def get(self, request):
        try:
            db_user_profile = get_profile(user=request.user)

        except Exception as e:
            return Response(
                {'detail': f"{e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(OutPutProfileSerializer(db_user_profile, context={"request": request}).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Profile",
        request=InputUpdateProfileSerializer,
        responses=OutPutProfileSerializer)
    def patch(self, request):
        serializer = InputUpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            db_user_profile = update_profile(
                request.user.profile,
                **serializer.validated_data
            )

        except Exception as e:
            return Response(
                {'detail': f"{e}"},
                 status=status.HTTP_400_BAD_REQUEST
            )

        return Response(OutPutProfileSerializer(db_user_profile, context={"request": request}).data, status=status.HTTP_200_OK)