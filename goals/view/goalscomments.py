from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from goals.models.goalscommets import GoalComment
from goals.permissions import CommentPermissions
from goals.serializers.comments_serializers import CommentsCreateSerializers, CommentsRUDSerializers


class GoalCommentsCreateView(CreateAPIView):
    """Создание комментария к цели пользователя"""
    model = GoalComment
    serializer_class = CommentsCreateSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: CommentsCreateSerializers) -> None:
        """Передаём в serializers новую переменную goal_id"""
        serializer.save(goal_id=self.request.data['goal'])


class GoalCommentsListView(ListAPIView):
    """Выводим список комментариев с фильтрами по целям"""
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsRUDSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self) -> None:
        """Запрос в БД, комментарии для выбранной цели"""
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentsRUDView(RetrieveUpdateDestroyAPIView):
    """Внесение изменений в комментарии пользователя, обновление, удаление, просмотр"""
    queryset = GoalComment.objects.all()
    serializer_class = CommentsRUDSerializers
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_queryset(self) -> GoalComment:
        """Запрос в БД, проверяем возможность внесения изменений"""
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )
