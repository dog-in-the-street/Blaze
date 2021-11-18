# 모든 요청을 받아들이는 비동기적인 WebSocket 소비자 역할을 하게된다. 
# 메시지를 클라이언트(브라우저)로부터 받아서 다시 클라이언트에게 전달하는 기능

# AsyncWebsocketConsumer를 사용함으로써 비동기적으로 함수가 동작하도록 함.
# 문제는 비동기적으로 동작하면 데이터베이스에 접근하는 것에 제한이 생기기 때문에 다른 조치가 필요함. 
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        room_name = self.room_name

        # save new messages
        @database_sync_to_async
        def save_message (self, room_name, user, message):
            return Message.objects.create(room=room_name, author=user, context=message)

        await save_message(self, room_name, user, message)

        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

       
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    