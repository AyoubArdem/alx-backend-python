import datetime 
import time
from django.http import JsonResponse
from django.utils import deltatime , timezone
from rest_framework.response import Response

class RequestLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        self.logger = None
    def __call__(self,requset):
        user = request.user if request.user.is_authenticated else "Annonymous"
        self.logger = f"{datetime.now()} - User: {user} - Path: {request.path}"
        with ("requests.log" , "a") as f:
            f.write(self.logger)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        allowed_start = datetime.strptime("06:00", "%H:%M").time()
        allowed_end = datetime.strptime("21:00", "%H:%M").time()

        response = self.get_response(request)
        if not (allowed_start <= now <= allowed_end):
            return JsonResponse(
                {"error": "Chat access allowed only between 6AM and 9PM."},
                status=403,
            )
        return response



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.window = 60  
        self.limit = 5
        self.cache = {} 

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR", "")
            now = time.time()

            timestamps = self.cache.get(ip, [])
         
            timestamps = [ts for ts in timestamps if now - ts < self.window]

            if len(timestamps) >= self.limit:
                return JsonResponse(
                    {"error": "Too many messages in the last minute."},
                    status=429
                )

            timestamps.append(now)
            self.cache[ip] = timestamps

 
        return self.get_response(request)

        
#methode01


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            if getattr(user, "role", None) not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": f"{user.username} is not authorized"},
                    status=403
                )
        else:
            return JsonResponse(
                {"error": "Anonymous users are not authorized"},
                status=403
            )

        return self.get_response(request)

#methode02
'''
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        
        if not user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication required."},
                status=403
            )

        
        user_role = getattr(user, "role", None)

        allowed_roles = ["admin", "moderator"]

        if user_role not in allowed_roles:
            return JsonResponse(
                {"error": "You do not have permission to access this resource."},
                status=403,
            )

        return self.get_response(request)
'''