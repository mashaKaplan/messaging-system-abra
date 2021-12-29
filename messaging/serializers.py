from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class GetMessagesInputSerializer(serializers.Serializer):
    send_messages = serializers.BooleanField(default=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = UserSerializer(source="sender", read_only=True)
    receiver_username = UserSerializer(source="receiver", read_only=True)

    class Meta:
        model = Message
        fields = ['content', 'subject', 'date_creation', 'is_read', 'receiver', 'sender',
                  'receiver_username', 'sender_username', ]
        read_only_fields = ['sender', 'sender_username', 'receiver_username', ]
