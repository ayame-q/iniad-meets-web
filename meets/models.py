from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from uuid import uuid4


# Create your models here.
class UserRole(models.Model):
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)


class User(AbstractUser):
    student_id = models.CharField(max_length=10, default="", null=True, blank=True, verbose_name="学籍番号")
    name = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="本名")
    display_name = models.CharField(max_length=20, default="No name", verbose_name="公開名")
    is_display_name_initialized = models.BooleanField(default=False, verbose_name="公開名初期化済み")
    entry_year = models.IntegerField(null=True, blank=True, verbose_name="入学年度")
    role = models.OneToOneField(UserRole, related_name="userinfo", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="権限")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    is_student = models.BooleanField(default=False, verbose_name="学生か")

    def get_class(self):
        if self.is_student:
            return self.entry_year - 2016
        else:
            return None


class Circle(models.Model):
    name = models.CharField(max_length=50, verbose_name="サークル名")
    leader_name = models.CharField(max_length=50, default="", verbose_name="代表者名")
    staff_users = models.ManyToManyField(UserRole, blank=True, related_name="staff_circles")
    admin_users = models.ManyToManyField(UserRole, blank=True, related_name="admin_circles")
    is_using_entry_form = models.BooleanField(default=True, verbose_name="内部エントリーフォームを利用する")
    entry_form_url = models.URLField(null=True, blank=True, verbose_name="エントリーフォームURL")
    panflet_url = models.URLField(null=True, blank=True, verbose_name="サークル資料URL")
    website_url = models.URLField(null=True, blank=True, verbose_name="WebサイトURL")


class ChatLog(models.Model):
    comment = models.TextField(verbose_name="コメント")
    send_user = models.ForeignKey(User, related_name="chat_logs", on_delete=models.CASCADE, verbose_name="送信者")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    receiver_circle = models.ForeignKey(Circle, related_name="questions", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="宛先サークル")
    parent = models.ForeignKey("self", related_name="replies", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="返信先")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名投稿")


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries", verbose_name="ユーザー")
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="entries", verbose_name="サークル")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")
