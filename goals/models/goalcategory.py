from django.db import models
from core.models import User
from goals.models.board import Board

class GoalCategory(models.Model):
    """Модель категорий пользователя"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
    board = models.ForeignKey(
        "Board", verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
