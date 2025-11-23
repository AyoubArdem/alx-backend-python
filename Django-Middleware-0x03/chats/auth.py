from rest_framework_simpletoken.tokens import RefreshToken
from django.contrib.auth.models import User

class get_tokens_for_users(User):
     refresh_token=RefreshToken.for_user(User)
     return {
       "refresh":str(refresh_token),
       "access":str(refresh_token.access_token),
     }
