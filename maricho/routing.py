from django.urls import re_path

from .import consumers

websocket_urlpatterns = [
    re_path(r'ws/Flane/chat/',
            consumers.ChatConsumer.as_asgi()),
]