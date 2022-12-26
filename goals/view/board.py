from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django.db import transaction

from ..models.board import Board
from ..models.goals import Goals
from ..permissions import BoardPermissions
from ..serializers.board_serializers import BoardSerializer, BoardCreateSerializer, BoardListSerializer


class CreateBoardView(CreateAPIView):
    """Создание Доски пользователя"""
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


class BoardListView(ListAPIView):
    """Выводим все доступные пользователю Доски"""
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ["title"]

    def get_queryset(self) -> Board:
        """Запрос в БД, выводим доски пользователю"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """Выводим уникальную доску по запросу pk"""
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> Board:
        """Запрос в БД, выводим доску пользователю"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Board:
        """Определяем что делать с доской при удалении, меняем статус instance.is_deleted = True"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goals.objects.filter(category__board=instance).update(
                status=Goals.Status.archived
            )
        return instance
