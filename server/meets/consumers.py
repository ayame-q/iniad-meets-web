from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone, html
from django.core.exceptions import ValidationError
import json, datetime, re, uuid
from .models import ChatLog, ChatLogReaction, Circle, Status, Question
from .views import get_status


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = "main"
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send_connect_messages()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        response = json.loads(text_data)

        for (event, data) in response.items():
            if event == "chat_message":
                comment = html.escape(data.get("comment"))
                is_anonymous = bool(data.get("is_anonymous"))
                sender_circle = None
                receiver_circle = None
                parent = None
                is_admin_message = bool(data.get("is_admin_message")) if self.user.is_superuser else False
                try:
                    if data.get("sender_circle_uuid"):
                        sender_circle = Circle.objects.filter(staff_users=self.user.role).get(uuid=data["sender_circle_uuid"])
                    if data.get("receiver_circle_uuid"):
                        receiver_circle = Circle.objects.get(uuid=data["receiver_circle_uuid"])
                except Circle.DoesNotExist:
                    pass
                if data.get("parent"):
                    try:
                        parent = ChatLog.objects.get(uuid=data["parent"])
                    except ChatLog.DoesNotExist:
                        pass

                chat_log = ChatLog.objects.create(comment=comment, send_user=self.user, sender_circle=sender_circle, receiver_circle=receiver_circle, parent=parent, is_anonymous=is_anonymous, is_admin_message=is_admin_message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_chat_message",
                        "data": json_dumps(chat_log.to_obj()),
                    }
                )
            elif event == "chat_reaction_add":
                chat_log_uuid = data.get("message_uuid")
                reaction = data.get("reaction")
                try:
                    chat_log = ChatLog.objects.get(uuid=chat_log_uuid)
                    chat_log_reaction = ChatLogReaction.objects.create(reaction=reaction, user=self.user, chat_log=chat_log)
                except (ChatLog.DoesNotExist, ValidationError):
                    continue
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_chat_reaction_add",
                        "data": json_dumps(chat_log_reaction.to_obj()),
                    }
                )
            elif event == "chat_reaction_remove":
                chat_log_uuid = data.get("message_uuid")
                reaction = data.get("reaction")
                try:
                    chat_log = ChatLog.objects.get(uuid=chat_log_uuid)
                    chat_log_reaction = ChatLogReaction.objects.get(reaction=reaction, user=self.user, chat_log=chat_log)
                    uuid = chat_log_reaction.uuid
                    chat_log_reaction.delete()
                    chat_log_reaction.uuid = uuid
                except ChatLog.DoesNotExist:
                    continue
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_chat_reaction_remove",
                        "data": json_dumps(chat_log_reaction.to_obj()),
                    }
                )
            elif event == "get_old_messages":
                oldest_uuid = data.get("oldest_uuid")
                await self.send_old_messages(oldest_uuid)

    async def send_connect_messages(self):
        chat_logs = reversed(ChatLog.objects.all().order_by("-created_at")[:30])
        circles = Circle.objects.all()
        await self.send(text_data=json_dumps({
            "init": {
                "user": self.user.to_obj(),
                "chat_logs": [chat_log.to_obj() for chat_log in chat_logs],
                "questions": [],
                "circles": [circle.to_obj() for circle in circles]
            }
        }))

    async def send_chat_message(self, event):
        data = event.get("data")
        await self.send(text_data=json_dumps({
            "chat_message": json.loads(data)
        }))

    async def send_chat_reaction_add(self, event):
        data = event.get("data")
        await self.send(text_data=json_dumps({
            "chat_reaction_add": json.loads(data)
        }))

    async def send_chat_reaction_remove(self, event):
        data = event.get("data")
        await self.send(text_data=json_dumps({
            "chat_reaction_remove": json.loads(data)
        }))

    async def send_old_messages(self, oldest_uuid):
        key_chat_log = ChatLog.objects.get(uuid=oldest_uuid)
        chat_logs = reversed(ChatLog.objects.filter(created_at__lt=key_chat_log.created_at).order_by("-created_at")[:30])
        await self.send(text_data=json_dumps({
            "old_messages": {
                "chat_logs": [chat_log.to_obj() for chat_log in chat_logs],
                "start_message_uuid": oldest_uuid
            }
        }))


    async def notify(self, event):
        notify = event["notify"]
        await self.send(text_data=json.dumps({
            "notify": notify
        }))

    async def status(self, event):
        status = event["status"]
        await self.send(text_data=json.dumps({
            "status": status
        }))

    async def start_broadcast(self, *args):
        await self.send(text_data=json.dumps({"start_broadcast": True}))

    async def force_reload(self, *args):
        await self.send(text_data=json.dumps({"force_reload": True}))

    async def end_event(self, *args):
        await self.send(text_data=json.dumps({"end_event": True}))


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError (f'Type {obj} not serializable')


def json_dumps(obj):
    return json.dumps(obj, default=json_serial)

