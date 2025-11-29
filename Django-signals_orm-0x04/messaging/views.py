
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Message

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return JsonResponse({"status": "User deleted"})

def UnreadMessagesManager(request,user_id):
    messages = Message.unread.for_user(user_id)
    data = [{"id":msg.id,"content":msg.content,"sender":msg.sender.username} for msg in messages]
    return JsonResponse({"unread messages":data})
