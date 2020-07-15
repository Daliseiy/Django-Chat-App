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
'''
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message

User  = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self,data):
        messages = Message.last_10_messages
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self,data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user,
            content = data['message']
        )
        content = {
            'command':'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self,messages):
        result =[]
        for message in messages:
            result.append(self.message_to_json(message))
        return result



    def message_to_json(self,message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp':str(message.timestamp)
        }


    commands = {
        'fetch_messages': fetch_messages,
        'new_messages': new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
       async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)


    def send_chat_message(self,message):
        #message = data['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
'''