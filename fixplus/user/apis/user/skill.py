from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.common.pagination import LimitOffsetPagination, get_paginated_response_context
from fixplus.job.selectors.job import search_job_list
from fixplus.job.serializers.job import InputJobSerializer, OutPutJobSerializer, InputJobParamsSerializer
from fixplus.job.services.job import create_job
from fixplus.user.selectors.skill import search_technician_skill, get_technician_skill
from fixplus.user.serializers.skill import InputTechnicianSkillParamsSerializer, OutputTechnicianSkillSerializer, \
    InputTechnicianSkillSerializer, InputUpdateTechnicianSkillSerializer
from fixplus.user.services.skill import create_technician_skill, update_technician_skill, delete_technician_skill


class TechnicianSkillListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician Skill",
        parameters=[InputTechnicianSkillParamsSerializer],
        responses=OutputTechnicianSkillSerializer)
    def get(self, request):
        query_serializer = InputTechnicianSkillParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        try:
            db_technician_skill_list = search_technician_skill(
                **query_serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianSkillSerializer,
            queryset=db_technician_skill_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create Technician Skill",
        request=InputTechnicianSkillSerializer,
        responses=OutputTechnicianSkillSerializer
    )
    def post(self, request):
        serializer = InputTechnicianSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            create_technician_skill(
                **serializer.validated_data
            )

            db_technician_skill_list = search_technician_skill(
                technician_id=serializer.validated_data.get('technician_id')
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianSkillSerializer,
            queryset=db_technician_skill_list,
            request=request,
            view=self,
        )


class TechnicianSkillDetailApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Update Technician Skill",
        request=InputUpdateTechnicianSkillSerializer,
        responses=OutputTechnicianSkillSerializer
    )
    def patch(self, request, uuid):
        serializer = InputUpdateTechnicianSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            technician_id = get_technician_skill(id=uuid).technician.id
            update_technician_skill(
                instance=get_technician_skill(id=uuid),
                **serializer.validated_data
            )

            db_technician_skill_list = search_technician_skill(
                technician_id=technician_id
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianSkillSerializer,
            queryset=db_technician_skill_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Delete Technician Skill",
        responses=OutputTechnicianSkillSerializer
    )
    def delete(self, request, uuid):
        try:
            technician_id = get_technician_skill(id=uuid).technician.id
            delete_technician_skill(
                instance=get_technician_skill(id=uuid),
            )

            db_technician_skill_list = search_technician_skill(
                technician_id=technician_id
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianSkillSerializer,
            queryset=db_technician_skill_list,
            request=request,
            view=self,
        )