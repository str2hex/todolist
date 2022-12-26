from typing import Any

from rest_framework import permissions
from django.contrib.sites import requests

from goals.models import GoalCategory, Goals, GoalComment
from goals.models.board import BoardParticipant, Board


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request: requests, view: Any, obj: Board) -> bool:
        """Проверка прав пользователя"""

        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request: requests, view: Any, obj: GoalCategory) -> bool:
        """Проверка прав пользователя"""
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request: requests, view: Any, obj: Goals) -> bool:
        """Проверка прав пользователя"""
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request: requests, view: Any, obj: GoalComment) -> bool:
        """Проверка прав пользователя"""
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
