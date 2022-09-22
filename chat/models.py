from django.db import models

class ChatNotification(models.Model):
    owner = models.ForeignKey('account.Researcher', null=True, blank=True, on_delete=models.SET_NULL, related_name="chat_owner")
    message = models.CharField(max_length=255, null=True, blank=True)
    unreads = models.PositiveIntegerField(default=0)
    collab = models.ForeignKey('account.Collab', null=True, blank=True, on_delete=models.SET_NULL, related_name="chat_notification_collab")
    sender = models.ForeignKey('account.Researcher', null=True, blank=True, on_delete=models.SET_NULL, related_name="chat_notification_sender")
    room = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.message)
        except:
            return str(self.id)

class Chat(models.Model):
    user = models.ForeignKey('account.Researcher', null=True, blank=True, on_delete=models.SET_NULL, related_name="author_messages")
    content = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('chat.ChatRoom', null=True, blank=True, on_delete=models.SET_NULL, related_name="room")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        try:
            return str(self.content)
        except:
            return str(self.id)

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all[:10]

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
