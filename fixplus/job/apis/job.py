from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.common.pagination import LimitOffsetPagination, get_paginated_response_context
from fixplus.job.selectors.selectors import search_job_list
from fixplus.job.serializers.job import InputJobSerializer, OutPutJobSerializer, InputJobParamsSerializer
from fixplus.job.services.job import create_job


class JobListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Job List",
        parameters=[InputJobParamsSerializer],
        responses=OutPutJobSerializer)
    def get(self, request):
        query_serializer = InputJobParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        try:
            db_customer_list = search_job_list(
                **query_serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutJobSerializer,
            queryset=db_customer_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create new job",
        request=InputJobSerializer,
        responses={201: OutPutJobSerializer, 400: {'detail': str}}
    )
    def post(self, request):
        serializer = InputJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            job_instances = create_job(
                added_by=request.user,
                **serializer.validated_data
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"result": _("Successfully placed in the assign queue.")}, status=status.HTTP_201_CREATED)