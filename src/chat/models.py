from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Message(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField()
    timestamp=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]

    