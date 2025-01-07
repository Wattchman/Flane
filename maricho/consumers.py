import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"chat_{self.scope['user'].id}"
        self.room_group_name = f"chat_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        recipient_id = data['recipient_id']

        recipient = await self.get_user(recipient_id)
        message = Message.objects.create(sender=self.scope['user'], recipient=recipient, content=content)

        await self.channel_layer.group_send(
            f"chat_{recipient_id}",
            {
                'type': 'chat_message',
                'content': content,
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'content': event['content'],
            'sender': event['sender'],
        }))

    @staticmethod
    async def get_user(user_id):
        return await User.objects.get(id=user_id)
