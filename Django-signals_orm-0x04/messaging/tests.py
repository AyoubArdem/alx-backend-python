from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Message


class MessageTest(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="ayoub", password="pass123")
        self.receiver = User.objects.create_user(username="ahmed", password="pass123")
        self.client.login(username="ayoub", password="pass123")
        self.client.login(username="ahmed", password="pass123")
        self.url = reverse("message-list")  

    def test_message_is_created(self):
        payload = {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "content": "hello world",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().content, "hello world")
