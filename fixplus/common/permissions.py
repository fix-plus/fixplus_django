from rest_framework.permissions import BasePermission


class AllowAny(BasePermission):
    message = ''
    def has_permission(self, request, view):
        return True



class IsVerifiedMobile(BasePermission):
    message = 'You not allowed to use this method, should be verified mobile.'
    def has_permission(self, request, view):
        if request.user.is_verified_mobile:
            return True


class IsVerified(BasePermission):
    message = 'You not allowed to use this method, should be verified e-mail.'
    def has_permission(self, request, view):
        if request.user.is_verified_mobile:
            return True