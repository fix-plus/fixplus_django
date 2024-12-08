from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.user.models import BaseUser
from fixplus.user.serializers.user import OutPutUserSerializer
from fixplus.user.services.group import assign_groups_to_user, remove_groups_from_user


class AssignGroupAPIView(IsSuperAdminOrAdminMixin, APIView):
    """
    API view to assign or remove groups from a user.
    """

    @extend_schema(
        summary="Assign Groups to a User",
        description="Assign one or more groups to a specific user. Accessible by Super Admin or Admins.",
        parameters=[
            OpenApiParameter(name='user_id', description='UUID of the user', required=True, type='uuid')
        ],
        request={
            'application/json': {
                'schema': serializers.Serializer,  # Dynamic schema based on input
                'example': {
                    'groups': ['admin', 'technician']
                }
            }
        },
    )
    def post(self, request, user_id):
        """
        Assign groups to a user.
        """
        user = get_object_or_404(BaseUser, pk=user_id)
        groups = request.data.get('groups', [])

        # Validate group names
        allowed_groups = ['super_admin', 'admin', 'technician']
        invalid_groups = [grp for grp in groups if grp not in allowed_groups]
        if invalid_groups:
            return Response({'detail': f'Invalid group names: {invalid_groups}'}, status=status.HTTP_400_BAD_REQUEST)

        # Delegate to service
        try:
            assign_groups_to_user(user, groups)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OutPutUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Remove Groups from a User",
        description="Remove one or more groups from a specific user. Accessible by Super Admin or Admins.",
        parameters=[
            OpenApiParameter(name='user_id', description='UUID of the user', required=True, type='uuid')
        ],
        request={
            'application/json': {
                'schema': serializers.Serializer,  # Dynamic schema based on input
                'example': {
                    'groups': ['admin', 'technician']
                }
            }
        },
    )
    def delete(self, request, user_id):
        """
        Remove groups from a user.
        """
        user = get_object_or_404(BaseUser, pk=user_id)
        groups = request.data.get('groups', [])

        # Validate group names
        allowed_groups = ['super_admin', 'admin', 'technician']
        invalid_groups = [grp for grp in groups if grp not in allowed_groups]
        if invalid_groups:
            return Response({'detail': f'Invalid group names: {invalid_groups}'}, status=status.HTTP_400_BAD_REQUEST)

        # Delegate to service
        try:
            remove_groups_from_user(user, groups)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OutPutUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
