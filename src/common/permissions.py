from rest_framework import permissions
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


class IsRegistered(BasePermission):
    message = _('You not allowed to use this method.')
    def has_permission(self, request, view):
        if request.user.is_admin or request.user.is_verified_mobile and request.user.registry_requests.exists and request.user.registry_requests.filter(status='approved').exists():
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


class MultiPermission(permissions.BasePermission):
    message = 'You do not have the required permissions to access this resource.'

    def __init__(self, *permissions_list):
        self.permissions_list = permissions_list

    def has_permission(self, request, view):
        if not self.permissions_list:
            return True

        return all(request.user.has_perm(perm) for perm in self.permissions_list)