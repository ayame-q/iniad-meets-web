from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Circle, ChatLog

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ("uuid", "name", "start_time_sec", "pamphlet", "website_url", "twitter_sn", "instagram_id", "comment")


class CircleAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ("uuid", "name", "leader_name", "pamphlet", "website_url", "twitter_sn", "instagram_id", "comment")


class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ()
