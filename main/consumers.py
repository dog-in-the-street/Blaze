# 모든 요청을 받아들이는 비동기적인 WebSocket 소비자 역할을 하게된다. 
# 메시지를 클라이언트(브라우저)로부터 받아서 다시 클라이언트에게 전달하는 기능
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import BlazeUser, ChatRoom, Message

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
        def save_message (self, user, room_name, message):
            # 채팅룸
            # ChatRoom에서 해당 이름이 없으면 ChatRoom을 새로 만들고 메시지 그 안에 넣기 
            chatroom_data, flag = ChatRoom.objects.get_or_create(chatroom_name=room_name)
            userForChatRoom = BlazeUser.objects.get(nickname=user.nickname)
            # flag가 True인 경우에는 인스턴스를 새로 만들어줌(create). False인 경우에는 이미 있는 인스턴스를 가져옴(get)
            if flag:
                # ChatRoom instance를 새로 만들어줬으니까 Message를 그 안에 넣어주기만 하면 됨. 
                Message.objects.create(chatroom=chatroom_data, author=user, room=room_name, context=message)
                # ChatRoom에서 User 정보 연결해주기(ManyToMany).
                chatroom_data.user.add(userForChatRoom)
                # 메시지 추가될 때마다 연결된 chatroom 수정하기(updated 시간 기록하기 위해서)
                chatroom_data.save()
            else:
                # 원래 해당 room_name을 가진 ChatRoom이 있기 때문에 Message만 추가해주면 됨.
                Message.objects.create(chatroom=chatroom_data, author=user, room=room_name, context=message)
                # ChatRoom에서 User 정보 연결해주기(ManyToMany).
                chatroom_data.user.add(userForChatRoom)
                # 메시지 추가될 때마다 연결된 chatroom 수정하기(updated 시간 기록하기 위해서)
                chatroom_data.save()
                
        await save_message(self, user, room_name, message);

        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.nickname
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

    