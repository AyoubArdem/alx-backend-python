
from django.contrib.auth.models import User
from django.http import JsonResponse

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return JsonResponse({"status": "User deleted"})
