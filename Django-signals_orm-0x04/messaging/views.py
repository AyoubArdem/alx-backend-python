from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import Message
from .utils import get_replies
from django.http import JsonResponse


def conversation_thread(request, user_id):
    messages = (
        Message.objects.filter(receiver_id=user_id, parent_message__isnull=True)
        .select_related("sender", "receiver")
        .prefetch_related(
            Prefetch("message_set", queryset=Message.objects.select_related("sender"))
        )
    )
    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "replies": get_replies(msg)
        })
    return JsonResponse({"threads:",data}}
                        
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return JsonResponse({"status": "User deleted"})

def UnreadMessagesManager(request,user_id):
    messages = Message.unread.for_user(user_id)
    data = [{"id":msg.id,"content":msg.content,"sender":msg.sender.username} for msg in messages]
    return JsonResponse({"unread messages":data})
