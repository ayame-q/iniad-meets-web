"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
#import django
#from channels.routing import get_default_application
import meets.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
#django.setup()
#application = get_default_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            meets.routing.websocket_urlpatterns
        )
    )
})
