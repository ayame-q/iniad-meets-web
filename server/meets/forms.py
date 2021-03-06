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
        #fields = ("name", "leader_name", "entry_user_name", "pamphlet", "website_url", "twitter_sn", "instagram_id", "comment")
        fields = ("name", "leader_name", "entry_user_name", "website_url", "twitter_sn", "instagram_id", "comment")

    def __init__(self, *args, **kwargs):
        super(CircleInfoForm, self).__init__(*args, **kwargs)
        #self.fields["pamphlet"].help_text = "16:9で1ページのPDFファイルがオススメです。"
        #self.fields["pamphlet"].widget.attrs["accept"] = "application/pdf"
        self.fields["comment"].help_text = "80文字以内かつ3行以内で入力してください。"

    def clean_comment(self):
        text = self.cleaned_data["comment"]
        if text.count("\n") >= 3:
            raise forms.ValidationError("3行以内で入力してください")
        if len(text) > 80:
            raise forms.ValidationError("80文字以内で入力してください")
        return text

    def clean_pamphlet(self):
        file = self.cleaned_data["pamphlet"]
        if file:
            _, ext = os.path.splitext(file.name)
            file.name = str(uuid4()) + ext.lower()
        return file


class CirclePamphletForm(BaseForm):
    class Meta:
        model = Circle
        fields = ("pamphlet",)

    def __init__(self, *args, **kwargs):
        super(CirclePamphletForm, self).__init__(*args, **kwargs)
        self.fields["pamphlet"].help_text = "16:9で1ページのPDFファイルがオススメです。"
        self.fields["pamphlet"].widget.attrs["accept"] = "application/pdf"
        self.fields["pamphlet"].widget.attrs["required"] = True

    def clean_pamphlet(self):
        file = self.cleaned_data["pamphlet"]
        if file:
            _, ext = os.path.splitext(file.name)
            file.name = str(uuid4()) + ext.lower()
        return file
