python
#!/usr/bin/env python3
from django.shortcuts import render
from restt_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import  MessageSerializer, ConversationSerializer
from .models import User, Message, Conversation
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]
    

   def get_queryset(self):
       user_id=self.request.query_params.get('user_id',None)
       if user_id is not None:
            Conversation.objects.filter(participants_id__user_id=user_id)
        return super().get_queryset()
    

class MessageViewSet(viewsets.ModelViewSet):
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]
    def get_queryset(self):
        return Message.object.filter(participants__user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        sender_ref = data.get("sender")
        conversation_ref = data.get("conversation")
       
        sender_obj = None
        if sender_ref:
            sender_obj = User.objects.filter(user_id=sender_ref).first()
            if not sender_obj:
                return Response({"detail": "Sender not found."}, status=status.HTTP_400_BAD_REQUEST)

        
        conv_obj = None
        if conversation_ref:
            conv_obj = Conversation.objects.filter(conversation_id=conversation_ref).first() 
            if not conv_obj:
                return Response({"detail": "Conversation not found."}, status=status.HTTP_400_BAD_REQUEST)
            is_participant = Message.objects.filte(conversation_id=conv_obj,conversation_participant=request.user).exists()
            if not is_participant :
                return Response({"you are not participant of this conversation"},status=status.HTTP_403_FORBIDDEN)
                

       
        serializer = self.get_serializer(data={
            "sender": sender_obj.pk if sender_obj else None,
            "conversation": conv_obj.pk if conv_obj else None,
            "message_body": data.get("message_body")
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

