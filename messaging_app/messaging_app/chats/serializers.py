python
#!/usr/bin/env python3
from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    read_only_fields = ("user_id", "created_at")
    def validate_password_hash(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate_email(self, value):
        if not value  or "@" not in value:
            raise serializers.ValidationError("Invalid email address.")
        return value



class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    read_only_fields = ("message_id", "sent_at")
    class Meta:
        model = Message
        fields = ("message_id", "sender", "conversation", "message_body", "sent_at")
        read_only_fields = ("message_id", "sent_at")

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value



class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        help_text="List of participant UUIDs (user_id) to create the conversation."
    )
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    read_only_fields = ("conversation_id", "created_at")
    
    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "participant_ids", "messages", "created_at")


    def validate_participant_ids(self, value):
        if not value or len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        for user_id in participant_ids:
            user = User.objects.get(user_id=user_id)
            conversation.participants_id.add(user)

        return conversation