from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions

from . import models, serializers
from .serializers import GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = models.GoalCategory
    serializer_class = serializers.GoalCategorySerializers
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(ListAPIView):
    model = models.GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return models.GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )