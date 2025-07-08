from typing import Sequence, Type, TYPE_CHECKING
from importlib import import_module

from channels.sessions import CookieMiddleware
from django.conf import settings
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import BaseAuthentication, CSRFCheck
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.db import database_sync_to_async

from src.common.permissions import IsVerifiedMobile, AllowAny, IsSuperAdmin, IsAdmin, IsSuperAdminOrAdmin, \
    IsTechnician, IsRegistered

def enforce_csrf(get_response):
    def middleware(request):
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        response = get_response(request)
        check.process_response(request, response)
        return response
    return middleware


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token


class CustomJWTPanelAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT_PANEL['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token


class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        # cookies are in scope, since we're wrapped in CookieMiddleware
        jwt_cookie = scope["cookies"].get(settings.JWT_AUTH_COOKIE)

        if not jwt_cookie:
            scope["account"] = AnonymousUser()
        else:
            try:
                authentication = JWTAuthentication()
                validated_token = authentication.get_validated_token(jwt_cookie)
                scope["account"] = await database_sync_to_async(authentication.get_user)(
                    validated_token
                )
            except Exception as e:
                # or raise validation errors, etc
                scope["account"] = AnonymousUser()

        return await self.inner(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return CookieMiddleware(JwtAuthMiddleware(inner))


# def get_auth_header(headers):
#     value = headers.get('Authorization')
#
#     if not value:
#         return None
#
#     auth_type, auth_value = value.split()[:2]
#
#     return auth_type, auth_value


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class AllowAnyMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
       JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (AllowAny, )


class IsVerifiedMobileMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsVerifiedMobile)


class IsRegisteredMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsRegistered)


class IsSuperAdminMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsSuperAdmin)


class IsAdminMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsAdmin)


class IsSuperAdminOrAdminMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsSuperAdminOrAdmin)


class IsTechnicianMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, IsTechnician)
