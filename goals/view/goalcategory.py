from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models.goalcategory import GoalCategory
from ..permissions import CategoryPermissions
from ..serializers.category_serializers import GoalCategorySerializers, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    """Создание категории пользователя"""
    model = GoalCategory
    serializer_class = GoalCategorySerializers
    permission_classes = [IsAuthenticated]


class GoalCategoryListView(ListAPIView):
    """Вывод списка категорий пользователя с фильтрами"""
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["board", "user"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self) -> GoalCategory:
        """Запрос в БД, выводим доступные категории пользователя"""
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Внесение изменений в категории пользователя, обновление, удаление, просмотр"""
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermissions]

    def get_queryset(self) -> GoalCategory:
        """Запрос в БД"""
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        """При удалении категории не удаляем из БД, меняем статус с False на instance.is_deleted = True"""
        instance.is_deleted = True
        instance.save()
        return instance
