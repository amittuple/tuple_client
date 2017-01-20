from django.db import models


class chat_store(models.Model):
    chat_message=models.CharField(max_length=999)
    chat_time=models.CharField(max_length=999)
    chat_sendby=models.CharField(max_length=100)
