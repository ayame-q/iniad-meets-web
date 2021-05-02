from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Circle, UserRole, ChatLog, ChatLogReaction, Entry, Status, Event, Question, QuestionSelection, QuestionResponse


class UUIDFieldAdmin(admin.ModelAdmin):
    readonly_fields=('uuid',)


class UserAdmin(UUIDFieldAdmin):
    list_display = ("username", "family_name", "given_name", "is_student", "entry_year")
    list_filter = ("is_student", "entry_year")


class CircleAdmin(UUIDFieldAdmin):
    list_display = ("name", "entry_user_name")


class ChatLogAdmin(UUIDFieldAdmin):
    list_display = ("comment", "send_user", "sender_circle", "receiver_circle", "created_at")
    search_fields = ("comment",)


class ChatLogReactionAdmin(UUIDFieldAdmin):
    list_display = ("reaction", "chat_log", "user")


class EntryAdmin(UUIDFieldAdmin):
    list_display = ("user", "circle", "created_at")


class QuestionAdmin(UUIDFieldAdmin):
    list_display = ("type", "text")
    list_display_links = ("type", "text")


class QuestionSelectionAdmin(UUIDFieldAdmin):
    list_display = ("text", "question", "is_correct")


class EventAdmin(UUIDFieldAdmin):
    list_display = ("start_time_sec", "type", "circle", "question", "pr_text")
    list_display_links = ("start_time_sec", "type")


class StatusAdmin(UUIDFieldAdmin):
    list_display = ("status", "opening_time", "started_time", "planning_start_time", "streaming_url", "archive_url")
    list_display_links = ("status", "opening_time")


admin.site.register(User, UserAdmin)
admin.site.register(Circle, CircleAdmin)
admin.site.register(UserRole, UUIDFieldAdmin)
admin.site.register(ChatLog, ChatLogAdmin)
admin.site.register(ChatLogReaction, ChatLogReactionAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSelection, QuestionSelectionAdmin)
admin.site.register(QuestionResponse, UUIDFieldAdmin)
