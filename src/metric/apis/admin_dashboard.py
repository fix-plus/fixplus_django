from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.account.serializers.technician_status import OutputTechnicianStatusSerializer, InputTechnicianStatusSerializer
from src.account.services.technician_status import create_technician_status
from src.common.mixins import IsVerifiedMobileMixin, IsSuperAdminOrAdminMixin
from src.metric.selectors.admin_dashboard import get_admin_dashboard_metric
from src.metric.serializers.admin_dashboard import OutputAdminDashboardMetricSerializer


class AdminDashboardMetricApi(IsSuperAdminOrAdminMixin, APIView):
    @extend_schema(
        summary="Get Admin Dashboard Metric",
        responses=OutputAdminDashboardMetricSerializer)
    def get(self, request):

        queryset = get_admin_dashboard_metric()

        return Response(OutputAdminDashboardMetricSerializer(queryset, context={"request": request}).data, status=status.HTTP_200_OK)