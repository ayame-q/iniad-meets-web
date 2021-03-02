from django import forms
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template.defaultfilters import safe
from datetime import timedelta
from .models import User, Circle, Entry
from django_boost.forms.mixins import FormUserKwargsMixin
from allauth.socialaccount.models import SocialAccount


class BaseForm(forms.ModelForm):
    def __init__(self, label_suffix="", *args, **kwargs):
        kwargs["label_suffix"] = label_suffix
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class UserNameForm(BaseForm):
    class Meta:
        model = User
        fields = ("name")


class UserDisplayNameForm(BaseForm):
    class Meta:
        model = User
        fields = ("display_name")

class EntryForm(BaseForm):
    class Meta:
        model = Entry
        fields = ("circle")