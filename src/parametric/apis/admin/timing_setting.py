from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.common.mixins import IsSuperAdminMixin
from src.parametric.selectors.timing_setting import get_timing_setting
from src.parametric.serializers.timing_setting import InputTimingSettingParametricSerializer, \
    OutPutTimingSettingParametricSerializer


class UpdateTimingSettingParametricApi(IsSuperAdminMixin, APIView):
    def patch(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'SUPER_ADMIN' not in user_groups:
            raise CustomAPIException(message=_('You are not allowed to use this method.'), status_code=status.HTTP_403_FORBIDDEN)

        instance = get_timing_setting()

        if not instance:
            raise CustomAPIException(message=_('Timing setting not found.'), status_code=status.HTTP_404_NOT_FOUND)

        serializer = InputTimingSettingParametricSerializer(instance, data=request.data, partial=True)  # Use partial=True for PATCH
        serializer.is_valid(raise_exception=True)

        serializer.save()  # Save the updated instance
        updated_instance = get_timing_setting()  # Fetch the updated instance

        return Response(OutPutTimingSettingParametricSerializer(updated_instance).data)