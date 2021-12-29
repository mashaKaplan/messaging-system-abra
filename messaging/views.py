from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer, GetMessagesInputSerializer


class NewMessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_sender = Q(sender=self.request.user)
        is_receiver = Q(receiver=self.request.user)
        messages = Message.objects.filter(is_sender | is_receiver)
        return messages

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        input_serializer = GetMessagesInputSerializer(data=self.request.query_params)
        input_serializer.is_valid(raise_exception=True)

        send_messages = input_serializer.validated_data.get('send_messages')

        if send_messages:
            messages = Message.objects.filter(sender=self.request.user)
        else:
            messages = Message.objects.filter(receiver=self.request.user)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        send_messages = Message.objects.filter(sender=self.request.user)
        received_messages = self.get_queryset()
        send_serializer = MessageSerializer(send_messages, many=True)
        received_serializer = MessageSerializer(received_messages, many=True)

        return JsonResponse({'send': send_serializer.data, 'received': received_serializer.data})

    @action(detail=False)
    def get_unread_messages(self, request, *args, **kwargs):
        messages = self.get_queryset().filter(is_read=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def read_message(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)


    # @action(detail=False)
    # def get_send_messages(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)