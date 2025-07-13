from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.mixins import IsVerifiedMobileMixin
from src.geo.serializers.user_location_tracker import InputUserLocationTrackerSerializer, \
    OutputUserLocationTrackerSerializer
from src.geo.services.user_location_tracker import create_user_location_tracker


class UserLocationTrackerApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Create User Location Tracker",
        request=InputUserLocationTrackerSerializer,
        responses=OutputUserLocationTrackerSerializer)
    def post(self, request):
        serializer = InputUserLocationTrackerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = create_user_location_tracker(
            user=request.user,
            **serializer.validated_data
        )

        return Response(OutputUserLocationTrackerSerializer(queryset, context={"request": request}).data, status=status.HTTP_201_CREATED)