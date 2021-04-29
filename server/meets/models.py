from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from slack_sdk import WebClient as SlackWebClient
from slack_sdk.errors import SlackApiError
from uuid import uuid4, UUID
import requests, json, os, datetime, hashlib


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4, verbose_name="UUID")

    class Meta:
        abstract = True


class UserRole(BaseModel):
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4, verbose_name="UUID")
    student_id = models.CharField(max_length=10, default="", null=True, blank=True, verbose_name="学籍番号")
    family_name = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="姓")
    given_name = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="名")
    family_name_ruby = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="姓(フリガナ)")
    given_name_ruby = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="名(フリガナ)")
    display_name = models.CharField(max_length=20, default="No name", verbose_name="公開名")
    is_display_name_initialized = models.BooleanField(default=False, verbose_name="公開名初期化済み")
    entry_year = models.IntegerField(null=True, blank=True, verbose_name="入学年度")
    role = models.OneToOneField(UserRole, related_name="userinfo", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="権限")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    is_student = models.BooleanField(default=False, verbose_name="学生か")
    slack_id = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name="Slack ID")

    def get_name(self):
        return self.family_name + " " + self.given_name

    def get_name_ruby(self):
        return self.family_name_ruby + " " + self.given_name_ruby

    def get_class(self):
        if self.is_student:
            return self.entry_year - 2016
        else:
            return None

    def get_slack_info(self):
        client = SlackWebClient(token=os.environ['SLACK_BOT_TOKEN'])
        try:
            response = client.users_lookupByEmail(email=self.email)
            self.slack_id = response["user"]["id"]
            self.save()
            return self.slack_id
        except SlackApiError:
            return None

    def get_question_count(self):
        return QuestionResponse.objects.filter(user=self, selection__question__type=1).count()

    def get_correct_count(self):
        return QuestionResponse.objects.filter(user=self, selection__question__type=1, selection__is_correct=True).count()

    def to_obj(self):
        return {
            "uuid": self.uuid,
            "display_name": self.display_name,
            "is_display_name_initialized": self.is_display_name_initialized,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "family_name_ruby": self.family_name_ruby,
            "given_name_ruby": self.given_name_ruby,
            "staff_circles": [circle.to_obj() for circle in self.role.staff_circles.all()] if self.role else [],
            "is_admin": self.is_superuser,
            "entered_circles": [{"uuid": entry.circle.uuid} for entry in self.entries.all()] if self.entries else []
        }


def get_circle_pamphlet_path(self, filename):
    prefix = 'pamphlet/'
    name = str(uuid4())
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_circle_thumbnail_path(self, filename):
    prefix = 'thumbnail/'
    name = str(uuid4())
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Circle(BaseModel):
    name = models.CharField(max_length=50, verbose_name="サークル名")
    leader_name = models.CharField(max_length=50, default="", verbose_name="代表者名")
    entry_user_name = models.CharField(max_length=50, default="", verbose_name="担当者名")
    staff_users = models.ManyToManyField(UserRole, blank=True, related_name="staff_circles", verbose_name="スタッフ")
    admin_users = models.ManyToManyField(UserRole, blank=True, related_name="admin_circles", verbose_name="管理者")
    website_url = models.URLField(null=True, blank=True, verbose_name="WebサイトURL")
    twitter_sn = models.CharField(max_length=15, null=True, blank=True, verbose_name="Twitter ID")
    instagram_id = models.CharField(max_length=30, null=True, blank=True, verbose_name="Instagram ID")
    comment = models.TextField(max_length=80, blank=True, default="", verbose_name="一言説明")
    pamphlet = models.FileField(null=True, blank=True, upload_to=get_circle_pamphlet_path, validators=[FileExtensionValidator(allowed_extensions=["pdf"])], verbose_name="サークル資料(PDF)")
    movie_uploaded_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name="動画アップロード時刻")
    logo_uploaded_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name="ロゴアップロード時刻")
    logo_url = models.URLField(null=True, blank=True, verbose_name="ロゴURL")
    thumbnail = models.ImageField(null=True, upload_to=get_circle_thumbnail_path, blank=True, verbose_name="サムネイル画像")
    entry_webhook = models.URLField(null=True, blank=True, verbose_name="登録時Webhook")
    entry_webhook_password = models.CharField(max_length=36, null=True, blank=True, verbose_name="登録時WebhookPassword")
    do_notify_join = models.BooleanField(default=True, verbose_name="入会者をSlackで通知する")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")

    class Meta:
        ordering = ["event__start_time_sec", "event__order"]

    def __str__(self):
        return self.name

    def to_obj(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "comment": self.comment,
            "pamphlet_url": self.pamphlet.url,
            "website_url": self.website_url,
            "twitter_sn": self.twitter_sn,
            "instagram_id": self.instagram_id,
            "thumbnail_url": self.thumbnail.url if self.thumbnail else None
        }


class ChatLog(BaseModel):
    comment = models.TextField(verbose_name="コメント")
    send_user = models.ForeignKey(User, related_name="chat_logs", on_delete=models.CASCADE, verbose_name="送信者")
    sender_circle = models.ForeignKey(Circle, related_name="chat_logs", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="送信元サークル")
    receiver_circle = models.ForeignKey(Circle, related_name="get_chat_logs", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="宛先サークル")
    parent = models.ForeignKey("self", related_name="replies", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="返信先")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名投稿")
    is_admin_message = models.BooleanField(default=False, verbose_name="運営メッセージ")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    reacted_users = models.ManyToManyField(User, through="ChatLogReaction", verbose_name="リアクション済みユーザー")

    def to_obj(self):
        return {
            "uuid": self.uuid,
            "comment": self.comment,
            "send_user_name": (self.send_user.display_name if not self.is_anonymous else "匿名") if not self.is_admin_message else "運営",
            "receiver_user": {
                "uuid": self.parent.send_user.uuid,
                "name": self.parent.send_user.display_name if not self.parent.is_anonymous else "匿名",
            } if self.parent else None,
            "sender_circle": {
                "uuid": self.sender_circle.uuid,
                "name": self.sender_circle.name
            } if self.sender_circle else None,
            "receiver_circle": {
                "uuid": self.receiver_circle.uuid,
                "name": self.receiver_circle.name
            } if self.receiver_circle else None,
            "is_admin_message": self.is_admin_message,
            "is_question": bool(self.receiver_circle),
            "is_answer": bool(self.parent and self.parent.receiver_circle and self.parent.receiver_circle == self.sender_circle),
            "parent": self.parent.to_obj() if self.parent else None,
            "reactions": [reaction.to_obj() for reaction in self.reactions.all()],
            "created_at": self.created_at
        }


reaction_accept_emojis = ["😀", "😆", "😅", "🤣", "😍", "☺️", "😉", "🥳", "🥺", "🤗", "🤔", "👏", "🤝", "👍", "🙏", "👀", "🙋", "🙇", "🍩", "💕", "⁉️", "✔️", "💯", "🆗", "🆖"]


class ChatLogReaction(BaseModel):
    chat_log = models.ForeignKey(ChatLog, related_name="reactions", on_delete=models.CASCADE, verbose_name="ログ")
    user = models.ForeignKey(User, related_name="reactions", on_delete=models.CASCADE, verbose_name="ユーザー")
    reaction = models.CharField(max_length=4, verbose_name="リアクション")

    def to_obj(self):
        return {
            "uuid": self.uuid,
            "chat_log_uuid": self.chat_log.uuid,
            "user": {
                "uuid": self.user.uuid,
                "name": self.user.display_name,
            },
            "reaction": self.reaction
        }

    def save(self, *args, **kwargs):
        if self.reaction not in reaction_accept_emojis:
            raise ValidationError("Not accepted emojis")
        if ChatLogReaction.objects.filter(chat_log=self.chat_log, user=self.user, reaction=self.reaction).exists():
            raise ValidationError("Cannot add many times same reaction")
        super(ChatLogReaction, self).save(*args, **kwargs)


class Entry(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries", verbose_name="ユーザー")
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="entries", verbose_name="サークル")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")

    def to_obj(self):
        return {
            "email": self.user.email,
            "full_name": self.user.get_name(),
            "family_name": self.user.family_name,
            "given_name": self.user.given_name,
            "family_name_ruby": self.user.family_name_ruby,
            "given_name_ruby": self.user.given_name_ruby,
            "student_id": self.user.student_id,
            "circle": {
                "uuid": self.circle.uuid,
                "name": self.circle.name,
            },
            "created_at": self.created_at
        }

    def save(self, *args, **kwargs):
        if Entry.objects.filter(circle=self.circle, user=self.user).exists():
            raise ValidationError("既に入会受付済みです。")
        if not self.user.family_name or not self.user.given_name:
            raise ValidationError("先に氏名を登録してください")
        result = super(Entry, self).save(*args, **kwargs)
        self.post_webhook()
        self.post_slack()
        return result

    def post_webhook(self):
        if self.circle.entry_webhook:
            dat = self.created_at.isoformat() + self.circle.entry_webhook_password
            token = hashlib.sha256(dat.encode()).hexdigest()

            headers = {
                'Content-Type': 'application/json',
                'Authentication': 'Token ' + token
            }
            try:
                requests.post(url=self.circle.entry_webhook, data=json_dumps(self.to_obj()), headers=headers)
            except Exception as err:
                print(err)

    def post_slack(self):
        client = SlackWebClient(token=os.environ['SLACK_BOT_TOKEN'])

        message = f"""{self.circle.name}の入会受付がありました。
> 氏名:　　　{self.user.get_name()}
> フリガナ:　{self.user.get_name_ruby()}
> 学籍番号:　{self.user.student_id}
> メール:　　{self.user.email}
> 受付日時:　{self.created_at.strftime("%Y-%m-%d %H:%M:%S")}

入会者リストを見る: {os.environ.get("SITE_HOST")}circle/admin/entries/{self.circle.uuid}
"""
        users = [user_role.userinfo.slack_id for user_role in self.circle.admin_users.all() if user_role.userinfo.slack_id]
        res = client.conversations_open(users=users)
        dm_id = res['channel']['id']
        try:
            client.chat_postMessage(channel=dm_id, text=message)
        except SlackApiError as e:
            print(f"Slack Error: {e.response['error']}")


question_type_choices = (
    (1, "クイズ"),
    (2, "アンケート")
)


class Question(BaseModel):
    type = models.SmallIntegerField(choices=question_type_choices, verbose_name="種類")
    text = models.TextField(default="", verbose_name="問題/質問")

    def __str__(self):
        return self.text + " (" + self.get_type_display() + ")"

    def responses(self):
        return QuestionResponse.objects.filter(selection__in=self.selections.all())

    def to_obj(self):
        result = {
            "uuid": self.uuid,
            "type": self.type,
            "text": self.text,
            "selections": [selection.to_obj() for selection in self.selections.all()],
        }
        if self.type == 1:
            result["correct_uuid"] = self.selections.get(is_correct=True).uuid
        return result

    def to_obj_start(self):
        return {
            "uuid": self.uuid,
            "type": self.type,
            "text": self.text,
            "selections": [selection.to_obj_start() for selection in self.selections.all()],
        }


class QuestionSelection(BaseModel):
    question = models.ForeignKey(Question, related_name="selections", on_delete=models.CASCADE, verbose_name="問題/質問")
    text = models.TextField(default="", verbose_name="選択肢")
    is_correct = models.BooleanField(default=False, verbose_name="正解か")

    def __str__(self):
        return self.text + " (" + self.question.text + ")"

    def percentage(self):
        if self.question.responses().count() == 0:
            return 0
        return int(self.responses.count() / self.question.responses().count() * 100)

    def to_obj(self):
        return {
            "uuid": self.uuid,
            "text": self.text,
            "percentage": self.percentage() if self.question.type == 2 else None,
            "question_uuid": self.question.uuid,
        }

    def to_obj_start(self):
        return {
            "uuid": self.uuid,
            "text": self.text,
            "question_uuid": self.question.uuid,
        }


class QuestionResponse(BaseModel):
    user = models.ForeignKey(User, related_name="question_responses", on_delete=models.CASCADE, verbose_name="クイズ・アンケート回答")
    selection = models.ForeignKey(QuestionSelection, related_name="responses", on_delete=models.CASCADE, verbose_name="選択")

    def is_correct(self):
        return self.selection.is_correct

    def to_obj(self):
        return {
            "selection_uuid": self.selection.uuid,
            "question_uuid": self.selection.question.uuid,
            "question_type": self.selection.question.type,
            "is_correct": bool(self.selection.is_correct)
        }


event_types = (
    ("circle_start", "サークル開始"),
    ("question_start", "クイズ・アンケート開始"),
    ("question_result", "クイズ解答・アンケート結果発表"),
    ("quiz_final_result", "クイズ最終結果発表"),
    ("tutorial_info_start", "情報画面チュートリアル開始"),
    ("tutorial_chat_start", "チャット画面チュートリアル開始"),
    ("tutorial_list_start", "サークルリストチュートリアル開始"),
    ("tutorial_hashtag_start", "ハッシュタグチュートリアル開始"),
    ("pr_url_start", "URL宣伝"),
    ("final_start", "最終画面表示")
)


class Event(BaseModel):
    type = models.CharField(max_length=30, choices=event_types, verbose_name="種類")
    start_time_sec = models.IntegerField(null=True, blank=True, verbose_name="開始時刻(秒)")
    order = models.IntegerField(null=True, blank=True, verbose_name="順番")
    circle = models.OneToOneField(Circle, related_name="event", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="サークル")
    question = models.ForeignKey(Question, related_name="event", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="クイズ/アンケート")
    pr_url = models.URLField(null=True, blank=True, verbose_name="広告URL")
    pr_text = models.TextField(null=True, blank=True, verbose_name="広告テキスト")

    class Meta:
        ordering = ["start_time_sec", "order"]

    def __str__(self):
        result = self.get_type_display()
        if self.circle:
            result += f" ({self.circle.name})"
        if self.question:
            result += f" ({self.question.text})"
        if self.pr_text:
            result += f" ({self.pr_text})"
        return result

    def get_starting_at(self):
        status = Status.objects.get()
        return timezone.localtime(status.started_time) + datetime.timedelta(seconds=self.start_time_sec)

    def to_obj(self):
        status = Status.objects.get()
        result = {
            "uuid": self.uuid,
            "type": self.type,
            "start_time_sec": self.start_time_sec,
            "starting_at": status.planning_start_time + datetime.timedelta(seconds=self.start_time_sec)
        }
        if status.started_time:
            result["starting_at"] = status.started_time + datetime.timedelta(seconds=self.start_time_sec)
        if self.type == "circle_start":
            result["circle"] = self.circle.uuid
        if self.type == "question_start":
            result["question"] = self.question.to_obj_start()
        if self.type == "question_result":
            result["question"] = self.question.to_obj()
        if self.type == "pr_url_start":
            result["pr_url"] = self.pr_url
            result["pr_text"] = self.pr_text
        return result


status_choices = (
    (0, "開場前"),
    (1, "開場可"),
    (2, "配信終了"),
)


class Status(BaseModel):
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="開催状況")
    opening_time = models.DateTimeField(null=True, blank=True, verbose_name="開場時間")
    started_time = models.DateTimeField(null=True, blank=True, verbose_name="実際のイベント開始日時")
    planning_start_time = models.DateTimeField(null=True, blank=True, verbose_name="イベント開始予定日時")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    streaming_url = models.CharField(max_length=512, null=True, blank=True, verbose_name="ストリーミングURL")
    archive_url = models.CharField(max_length=512, null=True, blank=True, verbose_name="アーカイブURL")
    can_circle_join = models.BooleanField(default=False, verbose_name="新規サークル受付中")
    can_circle_movie_upload = models.BooleanField(default=False, verbose_name="動画アップロード受付中")
    can_circle_pamphlet_upload = models.BooleanField(default=False, verbose_name="資料アップロード受付中")
    can_circle_logo_upload = models.BooleanField(default=False, verbose_name="ロゴアップロード受付中")

    @classmethod
    def get_instance(cls):
        cls.objects.get()


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError (f'Type {obj} not serializable')


def json_dumps(obj):
    return json.dumps(obj, default=json_serial)
