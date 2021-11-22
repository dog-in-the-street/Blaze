from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # websocket urlpattern에서는 path나 re_path를 사용함. 
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]