from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminMixin, IsRegisteredMixin
from src.parametric.selectors.timing_setting import get_timing_setting
from src.parametric.serializers.timing_setting import OutPutTimingSettingParametricSerializer


class GetTimingSettingParametricApi(IsRegisteredMixin, APIView):
    @extend_schema(
        summary="Get Timing Setting List",
        responses=OutPutTimingSettingParametricSerializer,
    )
    def get(self, request):
        query_set = get_timing_setting()

        return Response(OutPutTimingSettingParametricSerializer(query_set).data)
