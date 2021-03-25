from django import forms
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template.defaultfilters import safe
from datetime import timedelta
from .models import User, Circle, Entry
from django_boost.forms.mixins import FormUserKwargsMixin
from allauth.socialaccount.models import SocialAccount
from uuid import uuid4
import os, re


class BaseForm(forms.ModelForm):
    def __init__(self, label_suffix="", *args, **kwargs):
        kwargs["label_suffix"] = label_suffix
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class CircleJoinForm(BaseForm):
    class Meta:
        model = Circle
        fields = ("name", "leader_name", "entry_user_name")


class CircleInfoForm(BaseForm):
    class Meta:
        model = Circle
        fields = ("name", "leader_name", "entry_user_name", "pamphlet", "website_url", "twitter_sn", "instagram_id", "comment")

    def __init__(self, *args, **kwargs):
        super(CircleInfoForm, self).__init__(*args, **kwargs)
        self.fields["pamphlet"].help_text = "16:9で1ページのPDFファイルがオススメです。"
        self.fields["pamphlet"].widget.attrs["accept"] = "application/pdf"

    def clean_pamphlet(self):
        file = self.cleaned_data["pamphlet"]
        _, ext = os.path.splitext(file.name)
        file.name = str(uuid4()) + ext.lower()
        return file
