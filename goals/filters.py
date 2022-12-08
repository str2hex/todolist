import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goals, GoalComment


class GoalDateFilter(rest_framework.FilterSet):
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

