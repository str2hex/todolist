from django.db import models
from core.models import User


# Create your models here.
class TgUser(models.Model):
    chat_id = models.IntegerField()
    user_ud = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
