from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.account.selectors.technician_skill import search_technician_skill, get_technician_skill
from src.account.serializers.skill import InputTechnicianSkillParamsSerializer, OutputTechnicianSkillSerializer, \
    InputTechnicianSkillSerializer, InputUpdateTechnicianSkillSerializer
from src.account.services.skill import create_technician_skill, update_technician_skill, delete_technician_skill


class TechnicianSkillListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician Skill",
        parameters=[InputTechnicianSkillParamsSerializer],
        responses=OutputTechnicianSkillSerializer)
    def get(self, request, uuid):
        query_serializer = InputTechnicianSkillParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        db_technician_skill_list = search_technician_skill(
            **query_serializer.validated_data,
            technician_id=uuid,
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
    def post(self, request, uuid):
        serializer = InputTechnicianSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_technician_skill(
            **serializer.validated_data,
            technician_id=uuid,
        )

        db_technician_skill_list = search_technician_skill(
            technician_id=serializer.validated_data.get('technician_id')
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
    def patch(self, request, skill_id):
        serializer = InputUpdateTechnicianSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_technician_skill = get_technician_skill(id=skill_id)
        update_technician_skill(
            instance=db_technician_skill,
            **serializer.validated_data
        )

        db_technician_skill_list = search_technician_skill(
            technician_id=db_technician_skill.user.id
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
    def delete(self, request, skill_id):
        db_technician_skill = get_technician_skill(id=skill_id)
        delete_technician_skill(
            instance=db_technician_skill,
        )

        db_technician_skill_list = search_technician_skill(
            technician_id=db_technician_skill.user.id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianSkillSerializer,
            queryset=db_technician_skill_list,
            request=request,
            view=self,
        )