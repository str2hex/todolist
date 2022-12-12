from django.db import models
from core.models import User
from goals.models.goals import Goals


class GoalComment(models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    id = models.AutoField(primary_key=True)
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE, verbose_name="Название цели")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
