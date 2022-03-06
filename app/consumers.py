from channels.generic.websocket import AsyncJsonWebsocketConsumer
from app.models import Message
from asgiref.sync import sync_to_async

class ChatAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.groupname = ""
        if str(self.scope['user']) > "harshraj":
            self.groupname = str(self.scope['user']) + "harshraj"
        else:
            self.groupname = "harshraj" + str(self.scope['user'])
        print(self.groupname)
        print(self.channel_name)
        self.channel_layer.group_add(self.groupname, self.channel_name)

        await self.accept()
        # print("ok")
    
    async def receive_json(self, content, **kwargs):
        print(content)
        self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'chat.msg',
                'message': content
            }
        )

    async def chat_msg(self, event):
        print("test",event)
        await self.send_json(event['message'])
    
    async def disconnect(self, code):
        print("Disconnect -", code)