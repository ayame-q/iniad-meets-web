from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Circle, ChatLog, Entry, User

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


class CircleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("circle",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("display_name", "family_name", "given_name", "family_name_ruby", "given_name_ruby", "is_display_name_initialized")
        read_only_fields = ("is_display_name_initialized",)
