from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content_preview", "timestamp", "read", "edited")
    list_filter = ("read", "edited", "timestamp")
    search_fields = ("sender__username", "receiver__username")
    ordering = ("-timestamp",)

   

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message_preview", "created_at", "seen")
    list_filter = ("seen", "created_at")
    search_fields = ("user__username")
    ordering = ("-created_at",)

    
