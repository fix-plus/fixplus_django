from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from src.common.apis import BasePermissionAPIView
from src.common.mixins import IsSuperAdminMixin, IsAdminMixin, IsSuperAdminOrAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.common.permissions import MultiPermission
from src.account.selectors.user import search_user_list, get_user
from src.account.serializers.user import OutPutUserSerializer, InputUserSerializer, InputUserParamsSerializer, \
    OutPutSuperAdminUserDetailSerializer
from src.account.services.user import update_user


class UserListApi(IsSuperAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search User",
        parameters=[InputUserParamsSerializer],
        responses=OutPutUserSerializer)
    def get(self, request):
        query_serializer = InputUserParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        db_user_list = search_user_list(
            **query_serializer.validated_data
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutUserSerializer,
            queryset=db_user_list,
            request=request,
            view=self,
        )


class UserDetailAPIView(IsSuperAdminMixin, BasePermissionAPIView):
    @extend_schema(
        summary="Get User Detail",
        responses=OutPutSuperAdminUserDetailSerializer)
    def get(self, request, uuid):
        queryset = get_user(id=uuid)

        return Response(OutPutSuperAdminUserDetailSerializer(queryset, context={"request": request}).data)

    @extend_schema(
        summary="Update User",
        request=InputUserSerializer,
        responses=OutPutSuperAdminUserDetailSerializer)
    def patch(self, request, uuid):
        permission_check = self.check_permissions('account.change_another')
        if permission_check:
            return permission_check

        serializer = InputUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_user = update_user(
            instance=get_user(id=uuid),
            **serializer.validated_data
        )

        return Response(OutPutSuperAdminUserDetailSerializer(db_user, context={"request": request}).data)
