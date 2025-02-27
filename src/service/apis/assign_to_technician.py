from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsRegisteredMixin
from src.common.pagination import get_paginated_response_context, LimitOffsetPagination

from src.service.serializers.assign_to_technician import InputAssignToTechnicianParamsSerializer
from src.service.services.assign_to_technician import assign_service_to_technician


class AssignServiceToTechnicianListApi(IsRegisteredMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    # @extend_schema(
    #     summary="Search Referred Job To Technician",
    #     parameters=[InputReferredJobParamsSerializer],
    #     responses=InputReferredJobParamsSerializer,
    # )
    # def get(self, request):
    #     user_groups = request.user.groups.values_list('name', flat=True)
    #
    #     if 'super_admin' in user_groups or 'admin' in user_groups:
    #         serializer = InputReferredJobParamsSerializer(data=request.query_params)
    #         serializer.is_valid(raise_exception=True)
    #
    #         query_set = search_referred_job_list(
    #             **serializer.validated_data
    #         )
    #         return get_paginated_response_context(
    #             pagination_class=self.Pagination,
    #             serializer_class=OutPutAdminReferredJobSerializer,
    #             queryset=query_set,
    #             request=request,
    #             view=self,
    #         )
    #
    #     if 'technician' in user_groups:
    #         serializer = InputPublicReferredJobParamsSerializer(data=request.query_params)
    #         serializer.is_valid(raise_exception=True)
    #
    #         query_set = search_referred_job_list(
    #             technician_id=request.user.id,
    #             **serializer.validated_data
    #         )
    #         return get_paginated_response_context(
    #             pagination_class=self.Pagination,
    #             serializer_class=OutPutTechnicianReferredJobSerializer,
    #             queryset=query_set,
    #             request=request,
    #             view=self,
    #         )
    #
    #     return Response({'detail': _('You are not allowed to use this method.')}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        summary="Assign Service To Technician",
        request=InputAssignToTechnicianParamsSerializer,
    )
    def patch(self, request, uuid):
        # Validator
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' not in user_groups and 'admin' not in user_groups:
            return Response({'detail': _('You are not allowed to use this method.')}, status=status.HTTP_403_FORBIDDEN)

        serializer = InputAssignToTechnicianParamsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Core
        assign_service_to_technician(
            service_id=uuid,
            technician_id=serializer.validated_data.get('technician_id'),
            assigned_by=request.user
        )

        # Response
        return Response({"result": _("Assigning to technician was successful.")}, status=status.HTTP_201_CREATED)