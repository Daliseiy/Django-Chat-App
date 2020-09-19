import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.contrib.auth import get_user_model

User  = get_user_model()
class ChatConsumer(WebsocketConsumer):

    def new_message(self,data):
        author = data['from']
        message = Message.objects.create(
            author = author,
            content = data['message'])
        content = {
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def message_to_json(self,message):
        return {
            'author': message.author,
            'content': message.content,
            'timestamp':str(message.timestamp)
        }

        

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.accept())

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.new_message(text_data_json)

        # Send message to room group
    def send_chat_message(self,message):
        print('this is message function')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message

            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
