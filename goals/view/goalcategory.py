from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models.goalcategory import GoalCategory
from ..permissions import CategoryPermissions
from ..serializers.category_serializers import GoalCategorySerializers, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializers
    permission_classes = [IsAuthenticated]


class GoalCategoryListView(ListAPIView):
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

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
