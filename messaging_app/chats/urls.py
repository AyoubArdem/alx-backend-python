python
#!/usr/bin/env python3
from rest_framework import routers.DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(DefaultRouter().register(r'conversations', ConversationViewSet).register(r'messages', MessageViewSet).urls)),
    
]
