from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class WSConsummer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('Coin', self.channel_name)
        await self.accept()
    
    async def disconnect(self,code):
        await self.channel_layer.group_discard('Coin', self.channel_name)       

    async def send_new_data(self, event):
        data = event['text']
        await self.send(json.dumps(data))
