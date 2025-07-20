"""Authentication classes for channels."""
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.utils.translation import gettext_lazy as _
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode

User = get_user_model()


class JWTAuthMiddleware:
    """Middleware to authenticate user for channels"""

    def __init__(self, app):
        """Initialize the app."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Authenticate the user based on JWT."""
        close_old_connections()
        try:
            # Decode the query string and get token parameter
            query_string = scope["query_string"].decode("utf8")
            token_list = parse_qs(query_string).get('token', None)
            if not token_list:
                scope['user'] = AnonymousUser()
                scope['error'] = str(_("No token provided"))
                return await self.app(scope, receive, send)

            token = token_list[0]
            # Decode the token to get the user ID
            data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # Get the user from database
            scope['user'] = await self.get_user(data['user_id'])
            if scope['user'].is_anonymous:
                scope['error'] = str(_("User not found"))
        except ExpiredSignatureError:
            scope['user'] = AnonymousUser()
            scope['error'] = str(_("Token has expired"))
        except (InvalidSignatureError, DecodeError):
            scope['user'] = AnonymousUser()
            scope['error'] = str(_("Invalid token"))
        except (TypeError, KeyError):
            scope['user'] = AnonymousUser()
            scope['error'] = str(_("Invalid token format"))
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """Return the user based on user ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """Wrap channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))