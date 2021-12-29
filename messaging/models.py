from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    content = models.TextField(max_length=250)
    subject = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_messages')

    def __str__(self):
        return self.subject

