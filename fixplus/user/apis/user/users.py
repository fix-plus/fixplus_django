from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from fixplus.common.apis import BasePermissionAPIView
from fixplus.common.mixins import IsSuperAdminMixin, IsAdminMixin, IsSuperAdminOrAdminMixin
from fixplus.common.pagination import LimitOffsetPagination, get_paginated_response_context
from fixplus.common.permissions import MultiPermission
from fixplus.user.selectors.user import get_user_list, get_user
from fixplus.user.serializers.user import OutPutUserSerializer, InputUserSerializer, InputUserParamsSerializer, \
    OutPutUserDetailSerializer
from fixplus.user.services.user import update_user


class UserListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search User",
        parameters=[InputUserParamsSerializer],
        responses=OutPutUserSerializer)
    def get(self, request):
        query_serializer = InputUserParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        try:
            db_user_list = get_user_list(
                **query_serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutUserSerializer,
            queryset=db_user_list,
            request=request,
            view=self,
        )


class UserDetailAPIView(IsSuperAdminOrAdminMixin, BasePermissionAPIView):
    @extend_schema(
        summary="Get User Detail",
        responses=OutPutUserDetailSerializer)
    def get(self, request, uuid):
        try:
            queryset = get_user(id=uuid)

        except Exception as ex:
            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(OutPutUserDetailSerializer(queryset, context={"request": request}).data)

    @extend_schema(
        summary="Update User",
        request=InputUserSerializer,
        responses=OutPutUserDetailSerializer)
    def patch(self, request, uuid):
        permission_check = self.check_permissions('user.change_another')
        if permission_check:
            return permission_check

        serializer = InputUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            db_user = update_user(
                instance=get_user(id=uuid),
                **serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(OutPutUserDetailSerializer(db_user, context={"request": request}).data)
