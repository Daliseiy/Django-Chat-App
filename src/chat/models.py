from django.db import models
from django.contrib.auth import get_user_model

"""
Creating a message model is not really neccessary especially in the case of an anonymous user
which i am using. Unless you want to save previous messages in the database, You can make use of this
"""

User = get_user_model()
class Message(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField()
    timestamp=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]

    