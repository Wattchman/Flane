from channels.generic.websocket import WebsocketConsumer
from channels.consumer import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.group_name = 'user_{}'.format(self.user.id)

        async_to_sync(self.channel_layer.group_add)
        (self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)
        (self.group_name, self.channel_name)


    def recieve(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'new_message':
            self.send(json.dumps(data['message']))

