from django.db import models

class ChatSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(primary_key=True, max_length=100)
    user=models.IntegerField(blank=False, null=True) 

class Message(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.IntegerField(blank=False, null=True) 

