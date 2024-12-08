from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _


class AllowAny(BasePermission):
    message = ''
    def has_permission(self, request, view):
        return True


class IsVerifiedMobile(BasePermission):
    message = _('You not allowed to use this method, should be verified mobile.')
    def has_permission(self, request, view):
        if request.user.is_verified_mobile:
            return True


class IsSuperAdmin(BasePermission):
    message = _('You not allowed to use this method.')
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='super_admin').exists()


class IsAdmin(BasePermission):
    message = _('You not allowed to use this method.')
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='admin').exists()


class IsSuperAdminOrAdmin(BasePermission):
    message = _('You not allowed to use this method.')
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.groups.filter(name='super_admin').exists() or
            request.user.groups.filter(name='admin').exists()
        )


class IsTechnician(BasePermission):
    message = _('You not allowed to use this method.')
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='technician').exists()