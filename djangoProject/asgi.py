import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # مدیریت درخواست‌های HTTP

})
