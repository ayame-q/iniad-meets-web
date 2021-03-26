from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from slack_sdk import WebClient as SlackWebClient
from slack_sdk.errors import SlackApiError
from uuid import uuid4
import requests, json, os


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4, verbose_name="UUID")

    class Meta:
        abstract = True


class UserRole(BaseModel):
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4, verbose_name="UUID")
    student_id = models.CharField(max_length=10, default="", null=True, blank=True, verbose_name="学籍番号")
    name = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="本名")
    display_name = models.CharField(max_length=20, default="No name", verbose_name="公開名")
    is_display_name_initialized = models.BooleanField(default=False, verbose_name="公開名初期化済み")
    entry_year = models.IntegerField(null=True, blank=True, verbose_name="入学年度")
    role = models.OneToOneField(UserRole, related_name="userinfo", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="権限")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    is_student = models.BooleanField(default=False, verbose_name="学生か")
    slack_id = models.CharField(max_length=10, null=True, blank=True, default=None, verbose_name="Slack ID")

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
            return self.slack_id
        except SlackApiError:
            return None


class Circle(BaseModel):
    name = models.CharField(max_length=50, verbose_name="サークル名")
    leader_name = models.CharField(max_length=50, default="", verbose_name="代表者名")
    entry_user_name = models.CharField(max_length=50, default="", verbose_name="担当者名")
    staff_users = models.ManyToManyField(UserRole, blank=True, related_name="staff_circles", verbose_name="スタッフ")
    admin_users = models.ManyToManyField(UserRole, blank=True, related_name="admin_circles", verbose_name="管理者")
    order = models.IntegerField(null=True, blank=True, verbose_name="順番")
    start_time_sec = models.IntegerField(null=True, blank=True, verbose_name="開始時刻(秒)")
    website_url = models.URLField(null=True, blank=True, verbose_name="WebサイトURL")
    twitter_sn = models.CharField(max_length=15, null=True, blank=True, verbose_name="Twitter ID")
    instagram_id = models.CharField(max_length=30, null=True, blank=True, verbose_name="Instagram ID")
    comment = models.TextField(blank=True, default="", verbose_name="一言説明")
    pamphlet = models.FileField(null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=["pdf"])], verbose_name="サークル資料(PDF)")
    movie_uploaded_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name="動画アップロード時刻")
    entry_webhook = models.URLField(null=True, blank=True, verbose_name="登録時Webhook")
    do_notify_join = models.BooleanField(default=True, verbose_name="入会者をSlackで通知する")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")


class ChatLog(BaseModel):
    comment = models.TextField(verbose_name="コメント")
    send_user = models.ForeignKey(User, related_name="chat_logs", on_delete=models.CASCADE, verbose_name="送信者")
    sender_circle = models.ForeignKey(Circle, related_name="chat_logs", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="送信元サークル")
    receiver_circle = models.ForeignKey(Circle, related_name="questions", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="宛先サークル")
    parent = models.ForeignKey("self", related_name="replies", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="返信先")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名投稿")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    reacted_users = models.ManyToManyField(User, through="ChatLogReaction", verbose_name="リアクション済みユーザー")


class ChatLogReaction(models.Model):
    chat_log = models.ForeignKey(ChatLog, related_name="reactions", on_delete=models.CASCADE, verbose_name="ログ")
    user = models.ForeignKey(User, related_name="reactions", on_delete=models.CASCADE, verbose_name="ユーザー")
    reaction = models.CharField(max_length=2, verbose_name="リアクション")


class Entry(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries", verbose_name="ユーザー")
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="entries", verbose_name="サークル")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")

    def __init__(self):
        if self.circle.entry_webhook:
            data = {}
            headers = {
                'content-type': 'application/json'
            }
            try:
                requests.post(url=self.circle.entry_webhook, data=json.dumps(data), headers=headers)
            except Exception as err:
                print(err)
        super(Entry, self).__init__()


question_type_choices = (
    (1, "クイズ"),
    (2, "アンケート")
)


class Question(BaseModel):
    type = models.SmallIntegerField(choices=question_type_choices, verbose_name="種類")
    text = models.TextField(verbose_name="問題/質問")
    start_time_sec = models.IntegerField(null=True, blank=True, verbose_name="開始時刻(秒)")
    thinking_time_sec = models.IntegerField(null=True, blank=True, verbose_name="検討時間(秒)")


class QuestionSelection(BaseModel):
    question = models.ForeignKey(Question, related_name="selections", on_delete=models.CASCADE, verbose_name="問題/質問")
    is_correct = models.BooleanField(verbose_name="正解か")


class QuestionAnswer(BaseModel):
    user = models.ForeignKey(User, related_name="question_answers", on_delete=models.CASCADE, verbose_name="クイズ・アンケート回答")
    selection = models.ForeignKey(QuestionSelection, related_name="answers", on_delete=models.CASCADE, verbose_name="選択")


status_choices = (
    (0, "開始前"),
    (1, "開催中"),
    (2, "終了"),
)


class Status(BaseModel):
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="開催状況")
    opening_time = models.DateTimeField(null=True, blank=True, verbose_name="開場時間")
    started_time = models.DateTimeField(null=True, blank=True, verbose_name="実際のイベント開始日時")
    planning_start_time = models.DateTimeField(null=True, blank=True, verbose_name="イベント開始予定日時")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
