from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..filters import GoalDateFilter
from ..models.goals import Goals
from ..permissions import GoalPermissions
from ..serializers.goals_serializers import GoalCreateSerializer, GoalListSerializers, GoalsRUDSerializers


class GoalCreateView(CreateAPIView):
    """Создание цели"""
    model = Goals
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """Вывод списка целей с фильтрами"""
    model = Goals
    permission_classes = [IsAuthenticated]
    serializer_class = GoalListSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["priority", "due_date"]
    ordering = ["priority", "due_date"]
    search_fields = ["title"]

    def get_queryset(self) -> Goals:
        """Запрос в БД выводим доступные цели пользователя"""
        return Goals.objects.filter(category__board__participants__user=self.request.user).exclude(
            status=Goals.Status.archived)


class GoalRUDlView(RetrieveUpdateDestroyAPIView):
    """Внесение изменений в цели пользователя, обновление, удаление, просмотр"""
    queryset = Goals.objects.all()
    serializer_class = GoalsRUDSerializers
    permission_classes = [IsAuthenticated, GoalPermissions]

    def perform_destroy(self, instance: Goals) -> Goals:
        """При удалении не чистим БД, присваиваем статус АРХИВ"""
        instance.status = Goals.Status.archived
        instance.save()
        return instance
