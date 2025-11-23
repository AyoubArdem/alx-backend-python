python
#!/usr/bin/env python3
from django.db import models
import uuid
from django.contrib.auth.user import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLES = (
        ('admin','Admin'),
        ('host','Host'),
        ('guest','Guest'),
    )
    user_id = models.AutoField(primary_key=True, default=uuid.uuid4, editable=False ,unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    password_hash = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=30,blank=True,null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='guest', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, default=CURRENT_TIMESTAMP)

    def __str__(self):
        return self.username

class Message(models.Model):
    message_id = models.AutoField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(blank=False, null=False)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE, related_name="messages")
    sent_at = models.DateTimeField(auto_now_add=True, default=CURRENT_TIMESTAMP)
   
    class Meta:
        ordering = ("sent_at",)

    def __str__(self):
        return f'Message {self.message_id} from {self.sender_id.username}'


class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True, default=CURRENT_TIMESTAMP)
    messages = models.ManyToManyField(Message, related_name='conversations', blank=True, null=True)

    class Meta:
        ordering = ("-created_at")

    def __str__(self):
        return f'Conversation {self.conversation_id} - Participants: {[user.username for user in self.participants_id.all()]} - Created at: {self.created_at}'

