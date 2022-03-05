from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive_json(self, content, **kwargs):
        print(content)
        await self.send_json({'test': "wow"})
    
    async def disconnect(self, code):
        print("Disconnect -", code)