from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.user.models import BaseUser
from fixplus.user.serializers.permission import OutPutPermissionSerializer
from fixplus.user.services.permission import assign_permissions_to_group, assign_permissions_to_user, \
    remove_permissions_from_group, remove_permissions_from_user


class AssignPermissionAPIView(IsSuperAdminOrAdminMixin, APIView):
    """
    API view to assign or remove permissions to/from groups or users.
    """

    @extend_schema(
        summary="Assign Permissions to a Group or User",
        description="""
        Assign one or more permissions to a specific group or user.

        **Permissions can be managed for:**
        - **Groups:** Assigning permissions to groups affects all users within the group.
        - **Users:** Assigning permissions directly to users for more granular control.
        """,
        request={
            'application/json': {
                'schema': serializers.Serializer,  # Dynamic schema based on target_type
                'example': {
                    'target_type': 'group',
                    'target_id': 'group_uuid',
                    'permissions': ['can_approve_tasks', 'can_access_chat']
                }
            }
        },
    )
    def post(self, request):
        """
        Assign permissions to a group or a user.
        """
        target_type = request.data.get('target_type')
        target_id = request.data.get('target_id')
        permissions = request.data.get('permissions', [])

        if target_type not in ['group', 'user']:
            return Response({'detail': 'Invalid target_type. Must be "group" or "user".'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate permissions
        valid_permissions = Permission.objects.filter(codename__in=permissions)
        if valid_permissions.count() != len(permissions):
            invalid = set(permissions) - set(valid_permissions.values_list('codename', flat=True))
            return Response({'detail': f'Invalid permissions: {list(invalid)}'}, status=status.HTTP_400_BAD_REQUEST)

        if target_type == 'group':
            group = get_object_or_404(Group, pk=target_id)

            # Admins can only assign permissions to Technician group
            if request.user.groups.filter(name='admin').exists() and group.name != 'technician':
                return Response({'detail': 'Admins can only manage Technician group.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Delegate to service
            try:
                assign_permissions_to_group(group, permissions)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            permissions_assigned = Permission.objects.filter(codename__in=permissions)
            serializer = OutPutPermissionSerializer(permissions_assigned, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif target_type == 'user':
            user = get_object_or_404(BaseUser, pk=target_id)

            # Admins can only assign permissions to Technician users
            if request.user.groups.filter(name='admin').exists() and not user.groups.filter(name='technician').exists():
                return Response({'detail': 'Admins can only manage permissions for Technician users.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Delegate to service
            try:
                assign_permissions_to_user(user, permissions)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            permissions_assigned = Permission.objects.filter(codename__in=permissions)
            serializer = OutPutPermissionSerializer(permissions_assigned, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Remove Permissions from a Group or User",
        description="""
        Remove one or more permissions from a specific group or user.

        **Permissions can be managed for:**
        - **Groups:** Removing permissions from groups affects all users within the group.
        - **Users:** Removing permissions directly from users for more granular control.
        """,
        request={
            'application/json': {
                'schema': serializers.Serializer,  # Dynamic schema based on target_type
                'example': {
                    'target_type': 'user',
                    'target_id': 'user_uuid',
                    'permissions': ['can_access_chat']
                }
            }
        },
    )
    def delete(self, request):
        """
        Remove permissions from a group or a user.
        """
        target_type = request.data.get('target_type')
        target_id = request.data.get('target_id')
        permissions = request.data.get('permissions', [])

        if target_type not in ['group', 'user']:
            return Response({'detail': 'Invalid target_type. Must be "group" or "user".'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate permissions
        valid_permissions = Permission.objects.filter(codename__in=permissions)
        if valid_permissions.count() != len(permissions):
            invalid = set(permissions) - set(valid_permissions.values_list('codename', flat=True))
            return Response({'detail': f'Invalid permissions: {list(invalid)}'}, status=status.HTTP_400_BAD_REQUEST)

        if target_type == 'group':
            group = get_object_or_404(Group, pk=target_id)

            # Admins can only remove permissions from Technician group
            if request.user.groups.filter(name='admin').exists() and group.name != 'technician':
                return Response({'detail': 'Admins can only manage Technician group.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Delegate to service
            try:
                remove_permissions_from_group(group, permissions)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            permissions_removed = Permission.objects.filter(codename__in=permissions)
            serializer = OutPutPermissionSerializer(permissions_removed, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif target_type == 'user':
            user = get_object_or_404(BaseUser, pk=target_id)

            # Admins can only remove permissions from Technician users
            if request.user.groups.filter(name='admin').exists() and not user.groups.filter(name='technician').exists():
                return Response({'detail': 'Admins can only manage permissions for Technician users.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Delegate to service
            try:
                remove_permissions_from_user(user, permissions)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            permissions_removed = Permission.objects.filter(codename__in=permissions)
            serializer = OutPutPermissionSerializer(permissions_removed, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
