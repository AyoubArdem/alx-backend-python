python
#!/usr/bin/env python3
from django.contrib import admin
from .models import User, Message, Conversation

#methode01
# Register your models here.
'''
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Conversation)
'''
#methode02

 @admin.register(User)
 class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'first_name', 'last_name', 'role', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender_id', 'conversation', 'sent_at')
    search_fields = ('message_body',)
    list_filter = ('sent_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    search_fields = ('conversation_id',)
    list_filter = ('created_at',)
    