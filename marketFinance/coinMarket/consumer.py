from channels.generic.websocket import AsyncJsonWebsocketConsumer
from random import randint
import json
from asyncio import sleep

class WSConsummer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print(self)
        await self.accept()
        # await self.channel_layer.group_add("users", self.channel_name)
        # self.user = self.scope["user"]
        while True:
            await self.send(json.dumps({'message': randint(1,100)}))
            await sleep(10)
    async def receive_json(self,context):
        data = json.loads(context)
        print(data)
