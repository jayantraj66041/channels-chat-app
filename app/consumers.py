from channels.generic.websocket import JsonWebsocketConsumer
from app.models import Message
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

class ChatAsyncWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.groupname = ""
        receiver = self.scope['url_route']['kwargs']['receiver']
        if str(self.scope['user']) > receiver:
            self.groupname = str(self.scope['user']) + receiver
        else:
            self.groupname = receiver + str(self.scope['user'])
        # print(self.groupname)
        # print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.groupname, 
            self.channel_name
        )

        self.accept()
        # print("ok")
    
    def receive_json(self, content, **kwargs):
        # print("first", content)

        content['sender'] = str(self.scope['user'])

        message = Message()
        message.msg = content['msg']
        message.sender = User.objects.get(username=content['sender'])
        message.receiver = User.objects.get(username=content['receiver'])
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.groupname,
            {
                'type': 'chat.msg',
                'message': content
            }
        )

    def chat_msg(self, event):
        # event['message']['sender'] = str(self.scope['user'])
        # print("test",event)
        self.send_json(event['message'])
    
    def disconnect(self, code):
        print("Disconnect -", code)