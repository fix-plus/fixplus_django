from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _


class BasePermissionAPIView(APIView):

    def check_permissions(self, *permission_codenames):
        if not permission_codenames:
            return None

        for perm in permission_codenames:
            # Ensure the permission codename is a string
            if not isinstance(perm, str):
                return Response(
                    {'detail': f'Invalid permission type: {perm}. It must be a string.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not self.is_valid_permission(perm):
                return Response(
                    {'detail': _('Invalid permission.')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            has_perm = self.request.user.has_perm(perm)
            if not has_perm:
                return Response(
                    {'detail': _('You do not have permission to perform this action.')},
                    status=status.HTTP_403_FORBIDDEN
                )
        return None

    def is_valid_permission(self, permission_codename):
        try:
            app_label, perm_name = permission_codename.split('.')
        except ValueError:
            return False

        try:
            # Check if the permission exists in the specified app
            Permission.objects.get(codename=perm_name, content_type__app_label=app_label)
            return True
        except Permission.DoesNotExist:
            return False