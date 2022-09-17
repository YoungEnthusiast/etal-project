import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatNotification

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, msg, sender):
        new_msg = Message.objects.create(sender=sender, message=msg)
        new_msg.save()
        return new_msg

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
        sender = text_data_json['sender']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )
async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    sender = text_data_json['sender']
    await self.channel_layer.group_send(self.room_group_name, {
        'type': 'chat_message',
        'message': message,
        'sender': sender
    })

async def chat_message(self, event):
    message = event['message']
    sender = event['sender']
    new_msg = await self.create_chat(sender, message)  # It is necessary to await creation of messages
    await self.send(text_data=json.dumps({
        'message': new_msg.message,
        'sender': new_msg.sender
    }))







    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
