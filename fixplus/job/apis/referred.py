from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsRegisteredMixin
from fixplus.common.pagination import get_paginated_response_context, LimitOffsetPagination
from fixplus.job.selectors.referred import search_referred_job_list
from fixplus.job.serializers.referred import InputReferredJobToTechnicianSerializer, InputReferredJobParamsSerializer, \
    OutPutAdminReferredJobSerializer, InputPublicReferredJobParamsSerializer, OutPutTechnicianReferredJobSerializer
from fixplus.job.services.referred import create_referred_job_to_technician_by_admin


class ReferredJobToTechnicianListApi(IsRegisteredMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Referred Job To Technician",
        parameters=[InputReferredJobParamsSerializer],
        responses=InputReferredJobParamsSerializer,
    )
    def get(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' in user_groups or 'admin' in user_groups:
            serializer = InputReferredJobParamsSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)

            query_set = search_referred_job_list(
                **serializer.validated_data
            )
            return get_paginated_response_context(
                pagination_class=self.Pagination,
                serializer_class=OutPutAdminReferredJobSerializer,
                queryset=query_set,
                request=request,
                view=self,
            )

        if 'technician' in user_groups:
            serializer = InputPublicReferredJobParamsSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)

            query_set = search_referred_job_list(
                technician_id=request.user.id,
                **serializer.validated_data
            )
            return get_paginated_response_context(
                pagination_class=self.Pagination,
                serializer_class=OutPutTechnicianReferredJobSerializer,
                queryset=query_set,
                request=request,
                view=self,
            )

        return Response({'detail': _('You are not allowed to use this method.')}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        summary="Referred Job To Technician by admin",
        request=InputReferredJobToTechnicianSerializer,
    )
    def post(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' not in user_groups and 'admin' not in user_groups:
            return Response({'detail': _('You are not allowed to use this method.')}, status=status.HTTP_403_FORBIDDEN)

        serializer = InputReferredJobToTechnicianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            referred_job = create_referred_job_to_technician_by_admin(
                admin=request.user,
                **serializer.validated_data
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"result": _("Successfully referred to technician.")}, status=status.HTTP_201_CREATED)
