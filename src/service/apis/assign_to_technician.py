from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsSuperAdminOrAdminMixin

from src.service.serializers.assign_to_technician import InputAssignToTechnicianParamsSerializer
from src.service.services.assign_to_technician import assign_service_to_technician


class AssignServiceToTechnicianApi(IsSuperAdminOrAdminMixin, APIView):
    @extend_schema(
        summary="Assign Service To Technician",
        request=InputAssignToTechnicianParamsSerializer,
    )
    def patch(self, request, uuid):
        # Validator
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'SUPER_ADMIN' not in user_groups and 'ADMIN' not in user_groups:
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