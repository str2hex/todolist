from django.db import models
from core.models import User


class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")


class Goals(models.Model):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    due_date = models.DateField(verbose_name="Дата выполнения")
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    category = models.ForeignKey(GoalCategory, verbose_name="категория", related_name='goals',
                                 on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")


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
