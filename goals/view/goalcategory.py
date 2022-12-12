from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from ..models.goalcategory import GoalCategory
from ..permissions import UserAuthenticated
from ..serializers.category_serializers import GoalCategorySerializers, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializers
    permission_classes = [IsAuthenticated, UserAuthenticated]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, UserAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance