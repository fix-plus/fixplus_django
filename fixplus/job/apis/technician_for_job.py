from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.common.pagination import get_paginated_response_context, LimitOffsetPagination
from fixplus.job.selectors.technician_for_job import search_technician_for_job
from fixplus.job.serializers.technician_for_job import InputTechnicianForJobParamsSerializer, \
    OutPutTechnicianForJobSerializer


class TechnicianForJobListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician for Job List",
        parameters=[InputTechnicianForJobParamsSerializer],
        responses=OutPutTechnicianForJobSerializer,
    )
    def get(self, request):
        query_serializer = InputTechnicianForJobParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        try:
            db_user_list = search_technician_for_job(
                **query_serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutTechnicianForJobSerializer,
            queryset=db_user_list,
            request=request,
            view=self,
        )
