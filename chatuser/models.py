from django.core.exceptions import ValidationError
from django.db import models
from Account.models import User


class Chat(models.Model):
    chat_id = models.SlugField(unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user2')


    def clean(self):
        if Chat.objects.filter(user1=self.user1, user2=self.user2).exists():
            raise ValidationError('این چت از قبل وجود دارد.')
        elif Chat.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValidationError('این چت از قبل وجود دارد.')

    def save(self, *args, **kwargs):
        if not self.chat_id:
            self.chat_id = f"{self.user1.id}{self.user2.id}"
        super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.user1} {self.user2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')

    def __str__(self):
        return f'{self.sender}: {self.content}'