from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone, html
import json, datetime, re
from .models import ChatLog, Circle, Status
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
        text_data_json = json.loads(text_data)
        if text_data_json.get("message") and text_data_json.get("message").get("comment"):
            message = text_data_json["message"]
            await self.send_chat_message(message)

        elif text_data_json.get("get_old"):
            id = text_data_json["get_old"]
            await self.send_old_messages(id)

        elif text_data_json.get("start_event"):
            if self.user.is_superuser:
                status = Status.objects.get(pk=1)
                status.status = 1
                status.started_time = timezone.localtime()
                status.save()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "status",
                        "status": json.dumps(get_status()),
                    }
                )

        elif text_data_json.get("update_status"):
            if self.user.is_superuser:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "status",
                        "status": json.dumps(get_status()),
                    }
                )

        elif text_data_json.get("start_broadcast"):
            if self.user.is_superuser:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "start_broadcast"
                    }
                )

        elif text_data_json.get("force_reload"):
            if self.user.is_superuser:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "force_reload"
                    }
                )

        elif text_data_json.get("notify") and text_data_json.get("notify").get("comment"):
            notify = text_data_json["notify"]
            comment = html.escape(notify["comment"])
            comment = re.sub("\r?\n", "<br>", comment)
            comment = re.sub("&lt;small&gt;(.*)&lt;/small&gt", "<small>\1</small>", comment)
            type = notify.get("type")
            color = notify.get("color")
            with_chat = bool(notify["with_chat"])
            try:
                timeout = int(notify["timeout"])
            except ValueError:
                timeout = False
            if self.user.is_superuser:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "notify",
                        "notify": json.dumps({
                            "comment": comment,
                            "type": type,
                            "timeout": timeout,
                            "color": color,
                        }),
                    }
                )
                if with_chat:
                    message = {
                        "comment": comment,
                        "sender_circle_pk": 17,
                    }
                    await self.send_chat_message(message)

    async def send_chat_message(self, message):
        comment = html.escape(message["comment"])
        is_anonymous = bool(message.get("is_anonymous"))
        sender_circle = None
        receiver_circle = None
        parent = None
        try:
            if message.get("sender_circle_pk"):
                sender_circle = Circle.objects.filter(staff_users=self.user.role).get(pk=message["sender_circle_pk"])
            if message.get("receiver_circle_pk"):
                receiver_circle = Circle.objects.get(pk=message["receiver_circle_pk"])
        except Circle.DoesNotExist:
            pass
        if message.get("parent_pk"):
            try:
                log = ChatLog.objects.get(pk=message["parent_pk"])
                if log.receiver_circle and log.receiver_circle != sender_circle:
                    raise ChatLog.DoesNotExist
                parent = log
            except ChatLog.DoesNotExist:
                pass

        log = ChatLog.objects.create(comment=comment, send_user=self.user, sender_circle=sender_circle, receiver_circle=receiver_circle, parent=parent, is_anonymous=is_anonymous)
        log = ChatLog.objects.get(pk=log.pk)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": json.dumps({
                    "id": log.id,
                    "comment": log.comment,
                    "receiver_circle_pk": log.receiver_circle.pk if log.receiver_circle else None,
                    "receiver_circle_name": log.receiver_circle.name if log.receiver_circle else None,
                    "sender_circle_pk": log.sender_circle.pk if log.sender_circle else None,
                    "sender_circle_name": log.sender_circle.name if log.sender_circle else None,
                    "is_anonymous": log.is_anonymous,
                    "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(log.created_at),
                    "parent_pk": log.parent.pk if log.parent else None,
                    "parent_user_name": (log.parent.send_user.display_name if not log.parent.is_anonymous else "匿名") if log.parent else None,
                    "parent_comment": log.parent.comment if log.parent else None,
                    "backend_send_user_pk": log.send_user.pk,
                    "backend_parent_user_pk": log.parent.send_user.pk if log.parent else None,
                    "send_user": {"display_name": log.send_user.display_name, "class": log.send_user.get_class()} if not log.is_anonymous else {"display_name": "匿名", "class": log.send_user.get_class()}
                }),
            }
        )

    async def chat_message(self, event):
        message_json = event["message"]
        message = json.loads(message_json)
        message["is_your_question"] = False
        message["is_your_answer"] = False
        if message["backend_send_user_pk"] == self.user.pk and message["receiver_circle_pk"]:
            message["is_your_question"] = True
        message.pop("backend_send_user_pk")
        if message["backend_parent_user_pk"] == self.user.pk:
            message["is_your_answer"] = True
        message.pop("backend_parent_user_pk")
        await self.send(text_data=json.dumps({
            "message": json.dumps(message)
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


    async def send_connect_messages(self):
        data = ChatLog.objects.all().order_by("-id")[:30]
        messages = [(
            {
                "id": message.id,
                "comment": message.comment,
                "receiver_circle_pk": message.receiver_circle.pk if message.receiver_circle else None,
                "receiver_circle_name": message.receiver_circle.name if message.receiver_circle else None,
                "sender_circle_pk": message.sender_circle.pk if message.sender_circle else None,
                "sender_circle_name": message.sender_circle.name if message.sender_circle else None,
                "is_anonymous": message.is_anonymous,
                "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(timezone.localtime(message.created_at)),
                "parent_pk": message.parent.pk if message.parent else None,
                "parent_user_name": (message.parent.send_user.display_name if not message.parent.is_anonymous else "匿名") if message.parent else None,
                "parent_comment": message.parent.comment if message.parent else None,
                "send_user": {"display_name": message.send_user.display_name, "class": message.send_user.get_class()} if not message.is_anonymous else {"display_name": "匿名", "class": message.send_user.get_class()}
            }
        ) for message in data]
        await self.send(text_data=json.dumps({"initial_messages": messages}))

    async def send_old_messages(self, id):
        data = ChatLog.objects.filter(id__lt=id).order_by("-id")[:30]
        messages = [(
            {
                "id": message.id,
                "comment": message.comment,
                "receiver_circle_pk": message.receiver_circle.pk if message.receiver_circle else None,
                "receiver_circle_name": message.receiver_circle.name if message.receiver_circle else None,
                "sender_circle_pk": message.sender_circle.pk if message.sender_circle else None,
                "sender_circle_name": message.sender_circle.name if message.sender_circle else None,
                "is_anonymous": message.is_anonymous,
                "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(timezone.localtime(message.created_at)),
                "parent_pk": message.parent.pk if message.parent else None,
                "parent_user_name": (message.parent.send_user.display_name if not message.parent.is_anonymous else "匿名") if message.parent else None,
                "parent_comment": message.parent.comment if message.parent else None,
                "send_user": {"display_name": message.send_user.display_name, "class": message.send_user.get_class()} if not message.is_anonymous else {"display_name": "匿名", "class": message.send_user.get_class()}
            }
        ) for message in data]
        await self.send(text_data=json.dumps({"old_messages": messages}))