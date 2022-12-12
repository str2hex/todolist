from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction

from ..models.board import Board
from ..models.goals import Goals
from ..permissions import UserAuthenticated, BoardPermissions
from ..serializers.board_serializers import BoardSerializer, BoardCreateSerializer, BoardListSerializer


class CreateBoardView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goals.objects.filter(category__board=instance).update(
                status=Goals.Status.archived
            )
        return instance
