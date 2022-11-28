from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from . import models, serializers


class GoalCategoryCreateView(CreateAPIView):
    model = models.GoalCategory
    serializer_class = serializers.GoalCategorySerializers
    permission_classes = [permissions.IsAuthenticated]
