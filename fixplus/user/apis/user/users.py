from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from fixplus.common.mixins import IsSuperAdminMixin
from fixplus.user.models import BaseUser
from fixplus.user.serializers.user import OutPutUserSerializer, InputUserSerializer


class UserListCreateAPIView(IsSuperAdminMixin, APIView):
    """
    API view to list all users and create a new user.
    """

    @extend_schema(
        summary="List All Users",
        description="Retrieve a list of all registered users. Only accessible by Super Admin.",
    )
    def get(self, request):
        users = BaseUser.objects.all()
        serializer = OutPutUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a New User",
        description="Register a new user by providing necessary details. Only accessible by Super Admin.",
        request=InputUserSerializer,
    )
    def post(self, request):
        serializer = InputUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output_serializer = OutPutUserSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(IsSuperAdminMixin, APIView):
    """
    API view to retrieve, update, or delete a specific user.
    """

    def get_object(self, pk):
        return get_object_or_404(BaseUser, pk=pk)

    @extend_schema(
        summary="Retrieve User Details",
        description="Get detailed information of a specific user by their ID. Only accessible by Super Admin.",
        parameters=[
            OpenApiParameter(name='pk', description='UUID of the user', required=True, type='uuid')
        ],
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = OutPutUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update User Information",
        description="Update the details of a specific user by their ID. Only accessible by Super Admin.",
        parameters=[
            OpenApiParameter(name='pk', description='UUID of the user', required=True, type='uuid')
        ],
        request=InputUserSerializer,
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = InputUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output_serializer = OutPutUserSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a User",
        description="Delete a specific user by their ID. Only accessible by Super Admin.",
        parameters=[
            OpenApiParameter(name='pk', description='UUID of the user', required=True, type='uuid')
        ],
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
