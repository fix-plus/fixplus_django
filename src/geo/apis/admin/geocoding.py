from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.mixins import IsVerifiedMobileMixin, IsSuperAdminOrAdminMixin
from src.geo.serializers.geocoding import OutputGeoCodingSerializer, InputParamsGeoCodingSerializer
from src.geo.serializers.user_location_tracker import InputUserLocationTrackerSerializer, \
    OutputUserLocationTrackerSerializer
from src.geo.services.user_location_tracker import create_user_location_tracker
from src.geo.source.geocoding import get_geocoding


class GeoCodingApi(IsSuperAdminOrAdminMixin, APIView):
    @extend_schema(
        summary="Get Geo Coding Location",
        parameters=[InputParamsGeoCodingSerializer],
        responses=OutputGeoCodingSerializer)
    def get(self, request):
        serializer = InputParamsGeoCodingSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        queryset = get_geocoding(
            **serializer.validated_data
        )

        return Response(OutputGeoCodingSerializer(queryset, context={"request": request}).data, status=status.HTTP_200_OK)