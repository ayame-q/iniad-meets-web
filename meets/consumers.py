from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone, html
import json, datetime
from .models import ChatLog, Circle



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = "main"
        if self.user.is_authenticated:
            print("Connected", self.user)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send_connect_message()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        comment = html.escape(message["comment"])
        is_anonymous = bool(message["is_anonymous"])
        receiver_circle = None
        if message["receiver_circle_pk"]:
            receiver_circle = Circle.objects.get(pk=message["receiver_circle_pk"])

        sync_to_async(ChatLog.objects.create(comment=comment, send_user=self.user, receiver_circle=receiver_circle, is_anonymous=is_anonymous))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": json.dumps({
                    "comment": comment,
                    "receiver_circle_pk": receiver_circle.pk if receiver_circle else None,
                    "receiver_circle_name": receiver_circle.name if receiver_circle else None,
                    "is_anonymous": is_anonymous,
                    "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),
                    "send_user": {"display_name": self.user.display_name, "class": self.user.get_class()} if not is_anonymous else {"display_name": "匿名", "class": self.user.get_class()}
                }),
            }
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))

    async def send_connect_message(self):
        data = ChatLog.objects.all().order_by("-id")[:50]
        messages = [(
            {
                "comment": message.comment,
                "receiver_circle_pk": message.receiver_circle.pk if message.receiver_circle else None,
                "receiver_circle_name": message.receiver_circle.name if message.receiver_circle else None,
                "is_anonymous": message.is_anonymous,
                "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(timezone.localtime(message.created_at)),
                "send_user": {"display_name": message.send_user.display_name, "class": message.send_user.get_class()} if not message.is_anonymous else {"display_name": "匿名", "class": message.send_user.get_class()}
            }
        ) for message in data]
        await self.send(text_data=json.dumps({"initial_messages": messages}))