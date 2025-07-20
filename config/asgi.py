import os

from config.env import env
from django.core.asgi import get_asgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('STAGE_PROJECT'))
asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter,URLRouter

from config.routing import websocket_urlpatterns
from src.common.middleware import JWTAuthMiddlewareStack


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})