import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models.goals import Goals


class GoalDateFilter(rest_framework.FilterSet):
    """Класс фильтра для категорий пользователя"""
    class Meta:
        model = Goals
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }

